from __future__ import annotations

from datetime import date, datetime, time, timedelta

import pandas as pd
import streamlit as st

from astronomy_planner.data import DEFAULT_EYEPIECES, DEFAULT_OBJECTS
from astronomy_planner.engine import recommend_targets

st.set_page_config(page_title="Astronomy Observing Planner", page_icon="🔭", layout="centered")

st.title("🔭 Practical Astronomy Observing Planner")
st.caption("Built for your Orion SpaceProbe 130ST at Moriarty, NM defaults.")

with st.sidebar:
    st.header("Session Inputs")
    lat = st.number_input("Latitude", value=34.99, format="%.4f")
    lon = st.number_input("Longitude", value=-106.05, format="%.4f")
    elevation_ft = st.number_input("Elevation (ft)", value=6200, step=100)

    obs_date = st.date_input("Date", value=date.today())
    start_t = st.time_input("Start time", value=time(20, 0))
    end_t = st.time_input("End time", value=time(22, 0))

    session_type = st.selectbox(
        "Session type",
        ["Quick 30-minute session", "Standard 1–2 hour session", "Deep session (3+ hours)"],
        index=1,
    )

    mode = st.selectbox(
        "Special mode",
        ["Balanced", "Showpiece Mode", "Planetary Mode", "Deep Sky Mode", "Quick Session Mode"],
    )

    top_n = st.slider("Number of targets", min_value=5, max_value=10, value=8)

start_dt = datetime.combine(obs_date, start_t)
end_dt = datetime.combine(obs_date, end_t)
if end_dt <= start_dt:
    end_dt = end_dt + timedelta(days=1)

if st.button("Build Tonight's Plan", type="primary", use_container_width=True):
    recommendations, moon_illum = recommend_targets(
        objects=DEFAULT_OBJECTS,
        lat=lat,
        lon=lon,
        elevation_ft=float(elevation_ft),
        start_dt=start_dt,
        end_dt=end_dt,
        session_type=session_type,
        mode=mode,
        eyepieces=DEFAULT_EYEPIECES,
        top_n=top_n,
    )

    if not recommendations:
        st.warning("No high-quality targets met your constraints. Extend time window or change mode.")
        st.stop()

    st.subheader("Tonight's Ranked Targets")
    st.write(f"Moon illumination: **{moon_illum * 100:.0f}%** (higher values reduce deep-sky contrast).")

    cards = []
    for idx, rec in enumerate(recommendations, start=1):
        filter_note = "UHC helpful" if rec.obj.uhc_helpful else "No UHC needed"
        barlow_note = " + 2x Barlow" if rec.use_barlow else ""
        cards.append(
            {
                "Rank": idx,
                "Object": rec.obj.name,
                "Type": rec.obj.object_type,
                "Constellation": rec.obj.constellation,
                "Best time": rec.best_time.strftime("%H:%M"),
                "Max alt": f"{rec.max_altitude:.0f}°",
                "Direction": rec.direction,
                "Difficulty": rec.difficulty,
                "Eyepiece": f"{rec.eyepiece}{barlow_note}",
                "Magnification": f"{rec.magnification:.0f}x",
                "TFOV": f"{rec.tfov:.2f}°",
                "Notes": f"{filter_note}. {rec.reason}",
            }
        )

    st.dataframe(pd.DataFrame(cards), use_container_width=True, hide_index=True)

    st.subheader("Start Here")
    st.success(f"Start with **{recommendations[0].obj.name}** for a fast confidence boost.")

    st.subheader("Tonight's Plan Checklist")
    for idx, rec in enumerate(recommendations, start=1):
        barlow_note = " +2x Barlow" if rec.use_barlow else ""
        filter_note = "Use UHC" if rec.obj.uhc_helpful else "No filter needed"
        st.markdown(
            f"- [ ] **{idx}. {rec.obj.name}** ({rec.obj.object_type}) at ~{rec.best_time.strftime('%H:%M')}  "
            f"  \\↳ {rec.eyepiece}{barlow_note}, {rec.magnification:.0f}x, {rec.direction}, max {rec.max_altitude:.0f}°, {filter_note}"
        )

st.markdown("---")
st.markdown(
    "**Practical scope logic:** this planner strongly favors bright, high-altitude, easy-to-find objects that look good in a 130 mm reflector."
)
