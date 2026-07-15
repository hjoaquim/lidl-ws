# Day 4 — Capstone: Build the Whole Thing 🏗️

Your team's mission: take the Superstore data **all the way** — ingest it, build
a **pipeline** that cleans and summarises it, **orchestrate** that pipeline with
**Airflow**, and put an interactive **dashboard** on top. Everything runs in
Codespaces — no setup.

This pulls together everything from Days 1–3. The scaffolding gives you the
shape; *you* fill in the logic.

## 1. Get your team's copy

1. One person: **Use this template → Create a new repository** (make it public).
2. **Code → Codespaces → Create codespace on main**. Wait ~2 min (it installs
   Airflow + the data libs).
3. Decide as a team how to collaborate — VS Code **Live Share**, one driver, or
   split the files and push. Your call.

## 2. Three commands you'll use

| Command | What it does |
|---------|--------------|
| `make pipeline` | Run the pipeline once (extract → transform → load) |
| `make up` | Start Airflow — UI on port **8080** (it prints an `admin` password) |
| `make dash` | Run the Streamlit dashboard — port **8501** |

The teaching notebook (`notebooks/01_teaching.ipynb`) covers ETL and Airflow —
work through it first.

## 3. The mission

**Must-have:**
1. **Pipeline** — implement `extract` / `transform` / `load` in `src/pipeline.py`.
   `make pipeline` should fill `output/` with `clean.csv` + summary files.
   *(This is your Day 2 cleaning, split into pipeline stages.)*
2. **Orchestrate** — complete `dags/superstore_dag.py` so the three stages run as
   Airflow tasks in order. `make up`, open the UI, **trigger `superstore_pipeline`**,
   and watch the tasks go green. (`dags/demo_dag.py` is a working example to copy.)
3. **Dashboard** — build `app.py` (KPIs + a region filter + a chart) reading
   `output/clean.csv`. `make dash` to see it. *(Day 3 again.)*

**Stretch:**
- Give the DAG a real `schedule` (e.g. `"@daily"`) and explain what changes.
- Add more charts / a category filter to the dashboard.
- **Deploy** the dashboard to Streamlit Community Cloud and share the link.

## 4. Show and tell

At the end, each team demos: trigger the DAG live, then show the dashboard. 🎉
