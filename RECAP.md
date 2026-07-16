# Python for Data Analytics — Workshop Recap

A 4-session (~3h) program taking practitioners from "beginner with Python" to
building and orchestrating a small analytics pipeline with a dashboard.

## Repositories

| Repo | Role | Branches |
|------|------|----------|
| [`lidl-ws`](https://github.com/hjoaquim/lidl-ws) | Course source of truth — all teaching material, build scripts, and solutions (`day-01…day-04/`) | `main` |
| [`superstore-cleanup-template`](https://github.com/hjoaquim/superstore-cleanup-template) | Day 2 attendee template | `main`, `solutions` |
| [`superstore-dashboard-template`](https://github.com/hjoaquim/superstore-dashboard-template) | Day 3 attendee template | `main`, `solutions` |
| [`superstore-pipeline-template`](https://github.com/hjoaquim/superstore-pipeline-template) | Day 4 capstone template | `main`, `solutions` |

All three template repos are **public** and flagged **Template repository** so
attendees can *Use this template*.

## The four days

| Day | Topic | Environment | What attendees do |
|-----|-------|-------------|-------------------|
| 1 | Python Foundations + Getting Data In | Google Colab | Python basics + pandas; load CSV / Excel / a Google Sheet |
| 2 | Manipulating & Cleaning Data | Codespaces | Clean the Superstore dataset (scripts) + a bonus ML notebook |
| 3 | Visualizing & Reporting | Codespaces | Build a Streamlit dashboard, deploy it to Streamlit Community Cloud |
| 4 | From Notebook to Pipeline (capstone) | Codespaces | **Group capstone:** pipeline → Airflow DAG → Streamlit dashboard |

Days 2–4 build on the same **Sample - Superstore** dataset (bundled in each
template — no download). Day 1 uses a small synthetic retail dataset.

## Solutions

Each template repo has a **`solutions` branch** with completed code — point
attendees there *after* each session. (In `lidl-ws`, the same solutions live
under `day-0X/solution/`.)

## Reminders (Day 4)

- Each attendee needs a **GitHub account with Codespaces** enabled. Nothing else.
- **One repo per group**; groups pick how to collaborate (Live Share / one driver).
- `make up` starts Airflow — it **holds the terminal** (use a 2nd terminal for
  `make pipeline` / `make dash`), takes ~60–90s, and prints the `admin` password.
- Validated in real Codespaces: Airflow UI loads, DAGs run green, dashboard serves.
- After the session, share the `solutions` branch link.
