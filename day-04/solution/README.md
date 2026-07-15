# Day 4 solutions

Completed versions of the three capstone files. Unlike Days 2–3 (which used
separate `*_solution.py` names), Day 4's solution **replaces the stubs at their
real paths** — the DAG imports `src.pipeline` and Streamlit runs `app.py`, so the
files must keep those names to actually run.

| Solution file | Target path in the repo |
|---------------|-------------------------|
| `pipeline.py` | `src/pipeline.py` |
| `superstore_dag.py` | `dags/superstore_dag.py` |
| `app.py` | `app.py` |

Everything else (`demo_dag.py`, the data, notebook, devcontainer, Makefile)
already lives on `main` unchanged.

## Build the `solutions` branch (on the template repo)

From the template repo, after you've pushed `main`:

```bash
git checkout -b solutions
cp <lidl-ws>/day-04/solution/pipeline.py       src/pipeline.py
cp <lidl-ws>/day-04/solution/superstore_dag.py dags/superstore_dag.py
cp <lidl-ws>/day-04/solution/app.py            app.py
git add -A && git commit -m "Add capstone solutions"
git push -u origin solutions
```

## Verified working (Airflow 2.10.5, in a container)

- `python -m src.pipeline` → writes `output/clean.csv` + summaries
- `superstore_pipeline` triggered in Airflow → `extract → transform → load` all
  succeed, `output/` produced
- `make dash` → Streamlit serves the dashboard with no errors
