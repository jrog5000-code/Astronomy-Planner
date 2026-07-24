"""Daily routine planning, reward scoring, and calendar helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Iterable, Literal

RoutineCategory = Literal["Task", "Meal", "Workout", "Habit", "Recovery"]


@dataclass(frozen=True)
class RoutineItem:
    """A repeatable routine entry that can be placed on a daily calendar."""

    name: str
    category: RoutineCategory
    start: time
    minutes: int
    points: int
    notes: str


@dataclass(frozen=True)
class ScheduledItem:
    """A routine entry assigned to a concrete calendar date."""

    item: RoutineItem
    start_dt: datetime
    end_dt: datetime
    reward_label: str


DEFAULT_ROUTINE: list[RoutineItem] = [
    RoutineItem("Wake, water, and sunlight", "Habit", time(7, 0), 15, 10, "Open curtains or step outside; drink water before caffeine."),
    RoutineItem("Breakfast", "Meal", time(7, 30), 30, 8, "Protein + fiber anchor meal."),
    RoutineItem("Top 3 priorities", "Task", time(8, 15), 15, 12, "Pick the three outcomes that would make today successful."),
    RoutineItem("Focused work block", "Task", time(9, 0), 90, 20, "Single-task, notifications off."),
    RoutineItem("Lunch", "Meal", time(12, 30), 30, 8, "Balanced plate; log meal idea for repeat use."),
    RoutineItem("Walk or mobility", "Workout", time(13, 15), 20, 12, "Easy movement to reset energy."),
    RoutineItem("Workout", "Workout", time(17, 30), 45, 25, "Strength, cardio, or planned class."),
    RoutineItem("Dinner", "Meal", time(19, 0), 40, 8, "Simple planned meal; prep tomorrow if possible."),
    RoutineItem("Reset space", "Task", time(20, 15), 15, 10, "Tidy high-friction surfaces and pack tomorrow's essentials."),
    RoutineItem("Wind-down", "Recovery", time(21, 30), 30, 15, "Screens down, stretch, read, or journal."),
]

MEAL_IDEAS = [
    "Greek yogurt bowl with berries and granola",
    "Egg scramble with toast and fruit",
    "Chicken rice bowl with vegetables",
    "Turkey wrap with salad",
    "Salmon, potatoes, and greens",
    "Bean chili with avocado",
    "Protein smoothie and oatmeal",
]

WORKOUT_ROTATION = [
    "Full-body strength: squat, push, hinge, pull, core",
    "Zone 2 cardio + 10 minutes mobility",
    "Upper body strength + brisk walk",
    "Lower body strength + stretching",
    "Intervals: short hard efforts with full recovery",
    "Long walk, hike, bike, or recreational sport",
    "Recovery mobility and easy steps",
]


def build_schedule(day: date, routine: Iterable[RoutineItem] = DEFAULT_ROUTINE) -> list[ScheduledItem]:
    """Return routine items ordered as a phone-friendly daily agenda."""

    scheduled: list[ScheduledItem] = []
    for item in routine:
        start_dt = datetime.combine(day, item.start)
        end_dt = start_dt + timedelta(minutes=item.minutes)
        scheduled.append(ScheduledItem(item=item, start_dt=start_dt, end_dt=end_dt, reward_label=reward_label(item.points)))
    return sorted(scheduled, key=lambda entry: entry.start_dt)


def reward_label(points: int) -> str:
    if points >= 20:
        return "Big win"
    if points >= 12:
        return "Momentum"
    return "Maintenance"


def score_day(completed_points: Iterable[int], available_points: Iterable[int]) -> tuple[int, int, int, str]:
    """Calculate earned points, possible points, percentage, and streak status."""

    earned = sum(completed_points)
    possible = sum(available_points)
    percent = round((earned / possible) * 100) if possible else 0
    if percent >= 90:
        status = "🔥 Streak builder"
    elif percent >= 70:
        status = "✅ Solid day"
    elif percent >= 40:
        status = "🌱 Keep going"
    else:
        status = "🧭 Reset gently"
    return earned, possible, percent, status


def week_dates(start_day: date) -> list[date]:
    """Return a seven-day calendar window starting on the selected day."""

    return [start_day + timedelta(days=offset) for offset in range(7)]
