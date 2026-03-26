"""Core astronomy logic for target filtering, ranking, and observing sequence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable, List, Literal

import numpy as np
from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body
from astropy.time import Time

from astronomy_planner.data import CatalogObject, DEFAULT_SCOPE, Eyepiece

SessionType = Literal["Quick 30-minute session", "Standard 1–2 hour session", "Deep session (3+ hours)"]
ModeType = Literal["Balanced", "Showpiece Mode", "Planetary Mode", "Deep Sky Mode", "Quick Session Mode"]


@dataclass
class Recommendation:
    obj: CatalogObject
    best_time: datetime
    max_altitude: float
    max_azimuth: float
    direction: str
    difficulty: str
    score: float
    reason: str
    eyepiece: str
    magnification: float
    tfov: float
    use_barlow: bool


def build_observer_location(lat: float, lon: float, elevation_ft: float) -> EarthLocation:
    return EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=(elevation_ft * 0.3048) * u.m)


def moon_illumination_fraction(sample_time: datetime) -> float:
    t = Time(sample_time)
    moon = get_body("moon", t)
    sun = get_body("sun", t)
    elongation = moon.separation(sun).rad
    return float((1 - np.cos(elongation)) / 2)


def _session_minutes(session_type: SessionType) -> int:
    if session_type == "Quick 30-minute session":
        return 30
    if session_type == "Deep session (3+ hours)":
        return 210
    return 120


def _difficulty_label(score: int) -> str:
    if score <= 1:
        return "easy"
    if score == 2:
        return "moderate"
    return "hard"


def _direction_from_azimuth(az: float) -> str:
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = int(((az + 22.5) % 360) / 45)
    return directions[idx]


def _score_object(
    obj: CatalogObject,
    max_alt: float,
    avg_alt: float,
    moon_illum: float,
    mode: ModeType,
) -> float:
    # Aggressive altitude filtering: heavily penalize low-altitude objects, because
    # real-world visual quality drops quickly through thicker atmosphere.
    if max_alt < 25:
        return -999

    score = 0.0
    if max_alt >= 50:
        score += 34
    elif max_alt >= 40:
        score += 24
    elif max_alt >= 30:
        score += 12

    score += max(0, avg_alt - 25) * 0.35

    # 130 mm reflector practicality: dim galaxies are deprioritized unless bright/core-heavy.
    if obj.object_type == "Galaxy":
        score -= 12
        if obj.magnitude > 8.0:
            score -= 8
        if obj.surface_brightness and obj.surface_brightness > 13:
            score -= 6

    if obj.magnitude <= 6.5:
        score += 12
    elif obj.magnitude <= 8.5:
        score += 6
    else:
        score -= 6

    score -= (obj.difficulty_base - 1) * 4
    if obj.showpiece:
        score += 8

    # Moon impact: nebulae and galaxies lose contrast as moon illumination rises.
    if moon_illum > 0.6 and obj.object_type in {"Galaxy", "Emission Nebula", "Reflection Nebula", "Emission/Reflection Nebula"}:
        score -= 10

    if mode == "Showpiece Mode" and obj.showpiece:
        score += 10
    if mode == "Planetary Mode" and obj.planetary_mode:
        score += 18
    if mode == "Planetary Mode" and obj.deep_sky:
        score -= 6
    if mode == "Deep Sky Mode" and obj.deep_sky:
        score += 8
    if mode == "Quick Session Mode":
        score += 6 if obj.difficulty_base <= 2 else -8

    return score


def _best_optics_for_object(obj: CatalogObject, eyepieces: Iterable[Eyepiece]) -> tuple[str, float, float, bool]:
    scope_f = DEFAULT_SCOPE["focal_length_mm"]
    preferred_mag = {
        "Open Cluster": 30,
        "Globular Cluster": 90,
        "Emission Nebula": 45,
        "Emission/Reflection Nebula": 50,
        "Planetary Nebula": 120,
        "Galaxy": 70,
        "Double Star": 120,
        "Double-Double": 170,
    }.get(obj.object_type, 70)

    best_name = "25 mm"
    best_mag = scope_f / 25
    best_tfov = 2.0
    best_err = 1e9
    best_barlow = False

    # Eyepiece recommendation logic: pick the focal length (and optional Barlow)
    # that lands closest to a practical target magnification for each object class.
    for ep in eyepieces:
        mag = scope_f / ep.focal_length_mm
        tfov = ep.apparent_fov_deg / mag
        for barlow in (False, True):
            trial_mag = mag * (2 if barlow else 1)
            if trial_mag > 260:
                continue
            err = abs(trial_mag - preferred_mag)
            if err < best_err:
                best_err = err
                best_name = ep.name
                best_mag = trial_mag
                best_tfov = tfov / (2 if barlow else 1)
                best_barlow = barlow

    return best_name, best_mag, best_tfov, best_barlow


def _with_planets(objects: list[CatalogObject], sample_time: datetime, observer: EarthLocation) -> list[CatalogObject]:
    planet_specs = [
        ("Moon", "Moon", "Solar System", -12.7, True),
        ("Jupiter", "Planet", "Solar System", -2.5, True),
        ("Saturn", "Planet", "Solar System", 0.8, True),
        ("Mars", "Planet", "Solar System", 1.2, True),
        ("Venus", "Planet", "Solar System", -4.0, True),
    ]
    dynamic = list(objects)
    t = Time(sample_time)
    for name, obj_type, const, mag, showpiece in planet_specs:
        body = get_body(name.lower(), t, observer)
        icrs = body.icrs
        dynamic.append(
            CatalogObject(
                name=name,
                object_type=obj_type,
                constellation=const,
                ra_h=float(icrs.ra.hour),
                dec_deg=float(icrs.dec.deg),
                magnitude=mag,
                surface_brightness=None,
                size_arcmin=20,
                difficulty_base=1,
                showpiece=showpiece,
                deep_sky=False,
                planetary_mode=True,
                uhc_helpful=False,
                notes="Solar system target computed for this date.",
            )
        )
    return dynamic


def recommend_targets(
    objects: list[CatalogObject],
    lat: float,
    lon: float,
    elevation_ft: float,
    start_dt: datetime,
    end_dt: datetime,
    session_type: SessionType,
    mode: ModeType,
    eyepieces: list[Eyepiece],
    top_n: int = 8,
) -> tuple[list[Recommendation], float]:
    observer = build_observer_location(lat, lon, elevation_ft)
    moon_illum = moon_illumination_fraction(start_dt)

    session_cap = _session_minutes(session_type)
    if (end_dt - start_dt).total_seconds() / 60 > session_cap:
        end_dt = start_dt + timedelta(minutes=session_cap)

    objects_live = _with_planets(objects, start_dt, observer)

    time_grid = Time([start_dt + timedelta(minutes=10 * i) for i in range(int((end_dt - start_dt).total_seconds() // 600) + 1)])

    recs: List[Recommendation] = []
    for obj in objects_live:
        coord = SkyCoord(ra=obj.ra_h * u.hourangle, dec=obj.dec_deg * u.deg)
        altaz = coord.transform_to(AltAz(obstime=time_grid, location=observer))
        altitudes = altaz.alt.deg
        azimuths = altaz.az.deg

        max_idx = int(np.argmax(altitudes))
        max_alt = float(altitudes[max_idx])
        avg_alt = float(np.mean(np.clip(altitudes, -90, 90)))

        score = _score_object(obj, max_alt, avg_alt, moon_illum, mode)
        if score < 0:
            continue

        eyepiece, mag, tfov, barlow = _best_optics_for_object(obj, eyepieces)

        diff_score = obj.difficulty_base + (1 if max_alt < 35 else 0) + (1 if obj.magnitude > 8.5 else 0)
        difficulty = _difficulty_label(diff_score)

        reason = (
            f"High point {max_alt:.0f}°, {obj.notes.lower()}"
            if max_alt >= 50
            else f"Worthwhile at {max_alt:.0f}° peak; keep timing tight for best contrast."
        )

        recs.append(
            Recommendation(
                obj=obj,
                best_time=time_grid[max_idx].to_datetime(),
                max_altitude=max_alt,
                max_azimuth=float(azimuths[max_idx]),
                direction=_direction_from_azimuth(float(azimuths[max_idx])),
                difficulty=difficulty,
                score=score,
                reason=reason,
                eyepiece=eyepiece,
                magnification=mag,
                tfov=tfov,
                use_barlow=barlow,
            )
        )

    recs.sort(key=lambda r: r.score, reverse=True)

    if mode == "Quick Session Mode":
        top_n = min(top_n, 5)
    elif session_type == "Quick 30-minute session":
        top_n = min(top_n, 5)

    selected = recs[:top_n]

    # Session optimization: observe closest-to-peak objects first to maximize quality
    # during short windows and avoid losing altitude-sensitive targets later.
    selected.sort(key=lambda r: abs((r.best_time - start_dt).total_seconds()))

    return selected, moon_illum
