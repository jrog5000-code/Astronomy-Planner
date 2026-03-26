"""Curated observing targets and equipment presets for the astronomy planner."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CatalogObject:
    """Static object data used for planning and ranking."""

    name: str
    object_type: str
    constellation: str
    ra_h: float
    dec_deg: float
    magnitude: float
    surface_brightness: float | None
    size_arcmin: float
    difficulty_base: int
    showpiece: bool
    deep_sky: bool
    planetary_mode: bool
    uhc_helpful: bool
    notes: str


@dataclass(frozen=True)
class Eyepiece:
    name: str
    focal_length_mm: float
    apparent_fov_deg: float


DEFAULT_OBJECTS: List[CatalogObject] = [
    CatalogObject("M42", "Emission Nebula", "Orion", 5.59, -5.45, 4.0, 13.0, 85, 1, True, True, False, True, "Bright core and wings; excellent in 130 mm."),
    CatalogObject("M45", "Open Cluster", "Taurus", 3.79, 24.12, 1.6, None, 110, 1, True, True, False, False, "Huge cluster; best at very low power."),
    CatalogObject("M44", "Open Cluster", "Cancer", 8.67, 19.67, 3.1, None, 95, 1, True, True, False, False, "Beehive cluster pops in wide field."),
    CatalogObject("M13", "Globular Cluster", "Hercules", 16.69, 36.47, 5.8, 12.4, 20, 1, True, True, False, False, "Resolves partially at medium/high power."),
    CatalogObject("M3", "Globular Cluster", "Canes Venatici", 13.70, 28.38, 6.2, 12.5, 18, 2, True, True, False, False, "Dense bright globular; easy star-hop."),
    CatalogObject("M5", "Globular Cluster", "Serpens", 15.31, 2.08, 5.7, 12.6, 23, 2, True, True, False, False, "Compact bright core, likes steady seeing."),
    CatalogObject("M11", "Open Cluster", "Scutum", 18.85, -6.27, 6.3, None, 14, 2, True, True, False, False, "Wild Duck cluster rich and bright."),
    CatalogObject("M31", "Galaxy", "Andromeda", 0.71, 41.27, 3.4, 13.5, 190, 2, True, True, False, False, "Core is easy, outer dust lanes need dark sky."),
    CatalogObject("M32", "Galaxy", "Andromeda", 0.71, 40.87, 8.1, 12.6, 8, 3, False, True, False, False, "Compact satellite galaxy near M31 core."),
    CatalogObject("M81", "Galaxy", "Ursa Major", 9.93, 69.07, 6.9, 13.2, 27, 3, False, True, False, False, "Bright galaxy core, pair with M82."),
    CatalogObject("M82", "Galaxy", "Ursa Major", 9.93, 69.68, 8.4, 12.7, 11, 3, True, True, False, False, "Cigar galaxy shape shows well in 130 mm."),
    CatalogObject("M51", "Galaxy", "Canes Venatici", 13.50, 47.20, 8.4, 13.0, 11, 4, False, True, False, False, "Companion visible; spiral hints only in excellent sky."),
    CatalogObject("M57", "Planetary Nebula", "Lyra", 18.89, 33.03, 8.8, 9.0, 1.4, 2, True, True, False, True, "Ring shape clear at moderate/high magnification."),
    CatalogObject("M27", "Planetary Nebula", "Vulpecula", 20.00, 22.72, 7.4, 11.0, 8, 2, True, True, False, True, "Dumbbell nebula loves UHC filter."),
    CatalogObject("M8", "Emission Nebula", "Sagittarius", 18.05, -24.38, 6.0, 13.0, 90, 2, True, True, False, True, "Lagoon bright with clustered stars."),
    CatalogObject("M20", "Emission/Reflection Nebula", "Sagittarius", 18.04, -23.02, 6.3, 12.8, 28, 3, False, True, False, True, "Trifid dark lanes need dark transparent sky."),
    CatalogObject("M17", "Emission Nebula", "Sagittarius", 18.34, -16.17, 6.0, 12.0, 20, 2, True, True, False, True, "Swan shape stands out with UHC."),
    CatalogObject("M16", "Open Cluster + Nebula", "Serpens", 18.31, -13.78, 6.4, 12.5, 35, 3, False, True, False, True, "Eagle nebula visible; pillars are photographic only."),
    CatalogObject("M35", "Open Cluster", "Gemini", 6.15, 24.33, 5.3, None, 28, 1, True, True, False, False, "Large rich cluster; good finder target."),
    CatalogObject("M37", "Open Cluster", "Auriga", 5.87, 32.55, 6.2, None, 24, 1, True, True, False, False, "Dense starfield, excellent at medium power."),
    CatalogObject("M36", "Open Cluster", "Auriga", 5.60, 34.13, 6.0, None, 12, 1, True, True, False, False, "Compact and bright in suburban skies."),
    CatalogObject("M38", "Open Cluster", "Auriga", 5.47, 35.84, 6.4, None, 21, 2, False, True, False, False, "Loose X-pattern cluster."),
    CatalogObject("M41", "Open Cluster", "Canis Major", 6.78, -20.73, 4.5, None, 38, 2, True, True, False, False, "Very bright winter cluster."),
    CatalogObject("M46", "Open Cluster", "Puppis", 7.70, -14.82, 6.1, None, 27, 2, False, True, False, False, "Cluster with tiny PN NGC 2438 nearby."),
    CatalogObject("M47", "Open Cluster", "Puppis", 7.60, -14.49, 4.4, None, 30, 1, True, True, False, False, "Sparse bright cluster, easy naked-eye area."),
    CatalogObject("M93", "Open Cluster", "Puppis", 7.74, -23.86, 6.0, None, 22, 2, False, True, False, False, "Triangular spray of stars."),
    CatalogObject("Albireo", "Double Star", "Cygnus", 19.51, 27.96, 3.1, None, 0.1, 1, True, False, True, False, "Gold/blue color contrast showpiece double."),
    CatalogObject("Mizar/Alcor", "Double Star", "Ursa Major", 13.40, 54.93, 2.2, None, 0.2, 1, True, False, True, False, "Classic easy double in Big Dipper."),
    CatalogObject("Epsilon Lyrae", "Double-Double", "Lyra", 18.74, 39.67, 4.7, None, 0.04, 3, True, False, True, False, "Needs stable seeing and higher power."),
    CatalogObject("NGC 869/884", "Open Cluster", "Perseus", 2.33, 57.13, 4.3, None, 60, 1, True, True, False, False, "Double Cluster is a binocular-like showpiece."),
    CatalogObject("NGC 457", "Open Cluster", "Cassiopeia", 1.32, 58.29, 6.4, None, 20, 1, False, True, False, False, "Owl/ET cluster; easy and fun."),
    CatalogObject("NGC 2392", "Planetary Nebula", "Gemini", 7.49, 20.91, 8.6, 9.0, 0.8, 3, False, True, False, True, "Eskimo PN handles magnification well."),
    CatalogObject("NGC 7662", "Planetary Nebula", "Andromeda", 23.43, 42.53, 8.3, 8.0, 0.6, 3, False, True, False, True, "Blue Snowball tiny but bright."),
]

DEFAULT_EYEPIECES: List[Eyepiece] = [
    Eyepiece("40 mm", 40.0, 43.0),
    Eyepiece("32 mm", 32.0, 50.0),
    Eyepiece("25 mm", 25.0, 52.0),
    Eyepiece("Zoom 21 mm", 21.0, 45.0),
    Eyepiece("Zoom 14 mm", 14.0, 55.0),
    Eyepiece("Zoom 7 mm", 7.0, 60.0),
    Eyepiece("3.2 mm UWA", 3.2, 82.0),
]

DEFAULT_SCOPE = {
    "name": "Orion SpaceProbe 130ST",
    "aperture_mm": 130,
    "focal_length_mm": 650,
    "f_ratio": 5.0,
}
