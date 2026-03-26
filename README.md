# Astronomy Observing Planner (Streamlit)

A practical, visual-observing-first planner for selecting the best targets tonight with a **130 mm Orion SpaceProbe 130ST**.

## Features
- Defaults to **Moriarty, NM** (`34.99, -106.05`, 6200 ft).
- Session inputs for date, time window, and session type.
- Curated target list (Messier + selected NGC + planets + double stars).
- Aggressive filtering to prioritize bright and high-altitude objects.
- Top ranked targets with practical notes, direction, difficulty, and best time.
- Eyepiece recommendation with magnification, TFOV, and optional Barlow.
- Modes: Balanced, Showpiece, Planetary, Deep Sky, Quick Session.
- “Tonight’s Plan” checklist output.

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
5. Open the generated URL on your phone and add it to home screen.

## Notes on ranking behavior
- Objects below ~25° are rejected.
- Strong preference for objects above 50° altitude.
- Dim galaxies are penalized for 130 mm aperture realism.
- Moon illumination reduces scores for low-contrast deep-sky objects.
