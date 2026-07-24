# Routine Rewards Calendar (Streamlit)

A phone-friendly daily routine app that turns recurring tasks, meal timing, meals, workouts, habits, and recovery into an easy reference calendar with simple reward points.

## Features
- Daily checklist with reward points for each routine item.
- Progress metrics for earned points, percent complete, streak status, and reward unlocks.
- Easy reference calendar covering tasks, meals, workouts, habits, and recovery.
- Meal timing table plus reusable meal idea rotation.
- Workout-of-the-day recommendation plus weekly workout preview.
- Optional custom item from the sidebar for one-off tasks.
- Mobile-friendly Streamlit layout that can be added to a phone home screen.

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown in terminal (usually `http://localhost:8501`).

## Deploy to Streamlit Cloud
1. Push this project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app**, pick your repo/branch, and set main file to `app.py`.
4. Deploy. Streamlit installs `requirements.txt` automatically.
5. Open the generated URL on your phone and add it to your home screen.

## Notes on rewards
- Small maintenance items keep momentum visible.
- Workouts and focused blocks carry larger point values.
- The daily reward goal is adjustable in the sidebar.
- Reward status is meant to encourage consistency, not perfection.
