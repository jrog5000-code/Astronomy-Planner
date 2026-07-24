from __future__ import annotations

from datetime import date, time

import pandas as pd
import streamlit as st

from astronomy_planner.routine import DEFAULT_ROUTINE, MEAL_IDEAS, WORKOUT_ROTATION, RoutineItem, build_schedule, score_day, week_dates

st.set_page_config(page_title="Routine Rewards Calendar", page_icon="✅", layout="centered")

st.title("✅ Routine Rewards Calendar")
st.caption("A phone-friendly daily routine hub for tasks, meals, meal timing, workouts, and momentum rewards.")

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {background: #1118270d; border-radius: 16px; padding: 12px;}
    .routine-card {border: 1px solid #e5e7eb; border-radius: 16px; padding: 14px; margin: 10px 0;}
    .routine-time {font-size: 0.85rem; color: #6b7280;}
    .routine-points {font-weight: 700; color: #16a34a;}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Plan Settings")
    plan_date = st.date_input("Calendar date", value=date.today())
    reward_goal = st.slider("Daily reward goal", min_value=40, max_value=150, value=100, step=5)
    focus = st.selectbox("Today's focus", ["Balanced", "Task heavy", "Meals + prep", "Workout priority", "Recovery day"])

    st.subheader("Add a quick custom item")
    custom_name = st.text_input("Item name", placeholder="e.g., Call Mom")
    custom_category = st.selectbox("Category", ["Task", "Meal", "Workout", "Habit", "Recovery"])
    custom_time = st.time_input("Time", value=time(16, 0))
    custom_minutes = st.number_input("Minutes", min_value=5, max_value=240, value=20, step=5)
    custom_points = st.number_input("Points", min_value=1, max_value=50, value=10, step=1)
    add_custom = st.checkbox("Include custom item today")

routine = list(DEFAULT_ROUTINE)
if add_custom and custom_name.strip():
    routine.append(
        RoutineItem(
            custom_name.strip(),
            custom_category,  # type: ignore[arg-type]
            custom_time,
            int(custom_minutes),
            int(custom_points),
            "Custom item added from the sidebar.",
        )
    )

schedule = build_schedule(plan_date, routine)

st.subheader("Today at a glance")
completed_names: list[str] = []
for entry in schedule:
    key = f"done-{entry.item.name}-{entry.start_dt.isoformat()}"
    if st.checkbox(
        f"{entry.start_dt.strftime('%I:%M %p')} · {entry.item.name} (+{entry.item.points})",
        key=key,
    ):
        completed_names.append(entry.item.name)

completed_points = [entry.item.points for entry in schedule if entry.item.name in completed_names]
available_points = [entry.item.points for entry in schedule]
earned, possible, percent, status = score_day(completed_points, available_points)

col1, col2, col3 = st.columns(3)
col1.metric("Points", f"{earned}/{possible}")
col2.metric("Progress", f"{percent}%")
col3.metric("Status", status)
st.progress(min(earned / reward_goal, 1.0), text=f"{earned} of {reward_goal} points toward today's reward")

if earned >= reward_goal:
    st.success("Reward unlocked: choose a guilt-free treat, hobby block, or relaxing wind-down.")
elif earned:
    st.info(f"{max(reward_goal - earned, 0)} points until your planned reward.")
else:
    st.info("Start with the smallest checkbox. Momentum counts.")

st.subheader("Easy reference calendar")
rows = []
for entry in schedule:
    rows.append(
        {
            "Time": f"{entry.start_dt.strftime('%I:%M %p')}–{entry.end_dt.strftime('%I:%M %p')}",
            "Category": entry.item.category,
            "Plan": entry.item.name,
            "Reward": f"{entry.item.points} pts · {entry.reward_label}",
            "Notes": entry.item.notes,
        }
    )
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.subheader("Meal timing and ideas")
meal_rows = [row for row in rows if row["Category"] == "Meal"]
st.dataframe(pd.DataFrame(meal_rows), use_container_width=True, hide_index=True)
st.write("Meal idea rotation:")
st.write(" · ".join(MEAL_IDEAS))

st.subheader("Workout reference")
weekday_index = plan_date.weekday()
st.success(f"Suggested workout today: **{WORKOUT_ROTATION[weekday_index]}**")
st.write("Weekly rotation:")
for day, workout in zip(week_dates(plan_date), WORKOUT_ROTATION, strict=False):
    st.markdown(f"- **{day.strftime('%a, %b %-d')}**: {workout}")

st.subheader("Weekly calendar preview")
week_rows = []
for day in week_dates(plan_date):
    day_schedule = build_schedule(day, routine)
    week_rows.append(
        {
            "Date": day.strftime("%a, %b %-d"),
            "Tasks": len([entry for entry in day_schedule if entry.item.category == "Task"]),
            "Meals": ", ".join(entry.start_dt.strftime("%-I:%M %p") for entry in day_schedule if entry.item.category == "Meal"),
            "Workout": WORKOUT_ROTATION[day.weekday()],
            "Points available": sum(entry.item.points for entry in day_schedule),
        }
    )
st.dataframe(pd.DataFrame(week_rows), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Tip: open this Streamlit app on your phone and add it to your home screen for app-like access.")
