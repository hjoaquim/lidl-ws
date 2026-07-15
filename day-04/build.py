"""Build the Day 4 teaching notebook.

    python build.py

The capstone scaffold (starter/) and reference solution (solution/) are
hand-maintained — a capstone is open-ended, so there's no gap generator here.
"""
from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

NOTEBOOKS = Path(__file__).parent / "starter" / "notebooks"


def md(t):
    return new_markdown_cell(t.strip("\n"))


def code(t):
    return new_code_cell(t.strip("\n"))


def build_notebook() -> None:
    cells = []
    C = cells.append

    C(md("""
# Day 4 — From Notebook to Pipeline
### Python for Data Analytics

Over three days you cleaned data and built a dashboard — running each step **by
hand**. Today you make it a **pipeline** that runs itself, and learn to
**orchestrate** it with **Airflow**. Then your team builds the whole thing
end-to-end.

**Agenda**
1. What's a data pipeline? (ETL / ELT)
2. From notebook to script
3. Why orchestrate — and what Airflow gives you
4. See Airflow live
5. Your capstone
"""))

    C(md("""
---
## 1. What's a data pipeline?

A **pipeline** is just a series of steps that run in order, on their own, every
time — no clicking through cells. The classic shape is **ETL**:

- **Extract** — get the raw data (a file, an API, a database)
- **Transform** — clean and reshape it
- **Load** — write the result somewhere useful (a warehouse, files a dashboard reads)

**ELT** is the same letters, reordered: load the raw data first, transform it
*inside* the warehouse later. Either way: the same steps, automated and repeatable.
"""))

    C(md("""
---
## 2. From notebook to script

A pipeline is nothing exotic — it's your functions, called in order. Here's the
whole idea in miniature:
"""))

    C(code("""
def extract():
    return [10, 20, 30, 40]          # pretend we read 4 rows

def transform(rows):
    return [r for r in rows if r >= 20]   # "clean": drop the small ones

def load(rows):
    print(f"Loaded {len(rows)} rows: {rows}")

# the pipeline = the steps, in order
load(transform(extract()))
"""))

    C(md("""
Move that out of the notebook into a `.py` file with a `run_all()` and you can
run the entire thing with **one command** — which is exactly what
`src/pipeline.py` does in your capstone repo (`make pipeline`).
"""))

    C(md("""
---
## 3. Why orchestrate?

`python pipeline.py` works. So why do teams reach for a tool like **Airflow**?
Because in the real world you also want:

- ⏰ **Scheduling** — run it every morning at 6am, automatically
- 🔁 **Retries** — a step fails (network blip)? retry it, don't lose the run
- 👀 **Monitoring** — a UI showing *which* step ran, when, and what broke
- 🔗 **Dependencies** — "don't transform until extract finished"
- ⏮️ **Backfills** — re-run last month on demand

An **orchestrator** runs your pipeline *for* you and watches over it.
"""))

    C(md("""
---
## 4. Airflow — DAGs

**Airflow** is the most common Python orchestrator. You describe your pipeline
as a **DAG** (Directed Acyclic Graph): **tasks** connected by **dependencies**,
with no loops.

Here's the demo DAG in your repo (`dags/demo_dag.py`) — three tasks wired in order:

```python
from airflow.decorators import dag, task

@dag(schedule=None, ...)
def demo_etl():
    @task
    def extract() -> int:
        return 100
    @task
    def transform(rows: int) -> int:
        return rows - 3
    @task
    def load(rows: int) -> None:
        print(f"Loaded {rows} rows.")

    load(transform(extract()))   # this wiring = extract >> transform >> load
demo_etl()
```

Each `@task` is a step; calling `load(transform(extract()))` tells Airflow the
**order**. The `@dag` settings (`schedule`, retries…) are the superpowers from
the last section.
"""))

    C(md("""
---
## 5. See it live 👀

Enough slides — let's watch it run.

**In the terminal:**
```bash
make up
```
This starts Airflow and prints an `admin` password. Open the **port 8080**
forwarded URL (a pop-up appears; or the Ports tab), log in, and:

1. Find the **`demo_etl`** DAG.
2. **Trigger** it (▶️ button).
3. Watch the tasks go **green** in the Graph view.
4. Click a task → **Logs** to see its output.

💬 That green graph is the whole point — you can *see* your pipeline run, catch
failures, and schedule it. Try triggering it again and watch a fresh run appear.
"""))

    C(md("""
---
## 6. Your capstone 🏗️

Now your team builds the real thing on the Superstore data — see the repo
`README.md`:

1. **Pipeline** — implement `extract/transform/load` in `src/pipeline.py`
   (`make pipeline`).
2. **Orchestrate** — wire `dags/superstore_dag.py`, then trigger
   `superstore_pipeline` in the Airflow UI and watch it go green.
3. **Dashboard** — build `app.py` (`make dash`).
4. **Stretch** — schedule the DAG, richer dashboard, deploy to Streamlit Cloud.

Everything you need you've already done across Days 1–3 — now it's yours to
assemble. Go build. 🚀
"""))

    nb = new_notebook(cells=cells)
    nb.metadata.update(
        {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        }
    )
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    out = NOTEBOOKS / "01_teaching.ipynb"
    nbformat.write(nb, out)
    print(f"  wrote {out} ({len(cells)} cells)")


if __name__ == "__main__":
    print("Building Day 4 teaching notebook...")
    build_notebook()
    print("Done.")
