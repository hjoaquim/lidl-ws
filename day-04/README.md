# Day 4 — From Notebook to Pipeline (trainer)

**3 hours.** Teaching block on ETL + orchestration with **Airflow** (live UI),
then a **group capstone**: teams take the Superstore data end-to-end —
pipeline → Airflow DAG → Streamlit dashboard. All in Codespaces.

## Shape of the day

| Time | Block |
|------|-------|
| ~10 min | Form groups, open the Codespace, `make up` (Airflow boots) |
| ~50 min | Teaching notebook — ETL/ELT, notebook→script, orchestration; **live Airflow**: open the UI, trigger `demo_etl`, watch tasks go green, explain schedule/retries/logs |
| ~100 min | **Capstone build** — implement `src/pipeline.py`, wire `dags/superstore_dag.py`, build `app.py` |
| ~25 min | Deploy + show-and-tell (each team triggers their DAG + demos the dashboard) |
| ~15 min | Course wrap / recap / feedback |

## How this folder is organised

```
day-04/
├── build.py            # generates the teaching notebook
├── starter/            # ← becomes the group TEMPLATE repo
│   ├── .devcontainer/  # Airflow 3 + Streamlit; installs on create; forwards 8080/8501
│   ├── Makefile        # make up / pipeline / dash / clean
│   ├── dags/demo_dag.py        # COMPLETE demo DAG (for the teaching live-demo)
│   ├── dags/superstore_dag.py  # STUB — groups wire it
│   ├── src/pipeline.py         # STUB — groups implement extract/transform/load
│   ├── app.py                  # STUB — groups build the dashboard
│   └── data/Sample - Superstore.csv
└── solution/           # COMPLETE pipeline.py, superstore_dag.py, app.py (solutions branch)
```

## Airflow on Codespaces (how it works)

- `make up` runs **`airflow standalone`** — **Airflow 2.10.5**, SQLite +
  SequentialExecutor, one command, UI on 8080. No docker-compose, no Postgres.
  It prints the `admin` password (also in `.airflow/standalone_admin_password.txt`).
  *(We use Airflow 2.10.5 rather than 3.x: its standalone reliably executes
  triggered DAGs, whereas Airflow 3.0.2's standalone crashes the scheduler on
  task execution.)*
- `AIRFLOW_HOME` and the DAGs folder are set in `devcontainer.json`
  (`containerEnv`) → `.airflow/` and `dags/` in the repo.
- **Codespaces proxy:** `make up` sets `AIRFLOW__WEBSERVER__BASE_URL` (and
  `ENABLE_PROXY_FIX`) to the forwarded `https://<codespace>-8080.<domain>` URL so
  the UI works behind the proxy.
- Validated in a container: standalone boots, UI serves, and triggering
  `superstore_pipeline` runs extract→transform→load to **success** via the
  scheduler (tasks go green), producing `output/`.

## Publishing the template repo (one-time)

Create a repo from `starter/`, mark it **Template repository**, and add a
`solutions` branch carrying the completed `src/pipeline.py`,
`dags/superstore_dag.py`, and `app.py` (from `solution/`).

## Regenerate the teaching notebook

`python build.py` (edits live in `build.py`'s cells). The scaffold and solution
files are hand-maintained (a capstone is open-ended — no gap generator).
