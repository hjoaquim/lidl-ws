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
**orchestrate** it with **Airflow**. Then your team builds the whole thing.

**Agenda**
1. What's a data pipeline? (ETL / ELT)
2. From notebook to script
3. Why orchestrate?
4. A DAG is not a cron job
5. Idempotency — the safety net
6. When things fail
7. Airflow: DAGs & tasks in code
8. Wiring tasks: ordering vs passing data
9. What Airflow is actually running
10. See it live
11. Your capstone
"""))

    # 1
    C(md("""
---
## 1. What's a data pipeline?

A **pipeline** is a series of steps that run in order, on their own, every time
— no clicking through cells. The classic shape is **ETL**:

- **Extract** — get the raw data (a file, an API, a database)
- **Transform** — clean and reshape it
- **Load** — write the result somewhere useful (a warehouse, files a dashboard reads)

**ELT** is the same letters reordered: load the raw data first, transform it
*inside* the warehouse later. Either way — the same steps, automated.
"""))

    # 2
    C(md("""
---
## 2. From notebook to script

A pipeline is nothing exotic — it's your functions, called in order. The whole
idea in miniature:
"""))

    C(code("""
def extract():
    return [10, 20, 30, 40]              # pretend we read 4 rows

def transform(rows):
    return [r for r in rows if r >= 20]  # "clean": drop the small ones

def load(rows):
    print(f"Loaded {len(rows)} rows: {rows}")

load(transform(extract()))               # the pipeline = the steps, in order
"""))

    C(md("""
Move that into a `.py` file with a `run_all()` and you can run the whole thing
with **one command** — exactly what `src/pipeline.py` does in your repo
(`make pipeline`).
"""))

    # 3
    C(md("""
---
## 3. Why orchestrate?

`python pipeline.py` works. So why do teams reach for **Airflow**? Because in
the real world, running by hand can't answer three questions:

| Question | By hand | With an orchestrator |
|----------|---------|----------------------|
| **What runs when?** | Someone remembers to run it | A schedule fires it — automatic, consistent |
| **What depends on what?** | "Everyone knows extract runs first" | Dependencies are written down and enforced |
| **What if it fails?** | Someone gets paged, debugs from scratch | Auto-retries, re-run just the failed step, logs kept |

> **The core idea:** orchestration doesn't add new logic — it takes the logic
> you already follow (order, error handling, scheduling) and makes it
> **reliable, repeatable, and observable**.
"""))

    # 4
    C(md("""
---
## 4. A DAG is not a cron job

The most common misconception: "Airflow is just a fancy cron." It isn't.

A **cron** fires each step at a fixed *time*:

```
00:00  extract      00:30  transform      01:00  load
```

What goes wrong:
- If `extract` takes 45 min instead of 30, `transform` starts on **stale/half-written data**.
- If `transform` **fails**, `load` runs anyway — on bad data.
- There's no "retry just the step that broke."

A **DAG** (Directed Acyclic Graph) encodes **dependencies**, not clock times:

```
extract  ──▶  transform  ──▶  load
```

- Each task starts only when its upstream task **succeeds**.
- If `transform` fails, `load` never runs — no wasted work, no bad data.
- You can retry `transform` alone and the run resumes from there.
"""))

    # 5
    C(md("""
---
## 5. Idempotency — the safety net

A pipeline is **idempotent** if running it twice gives the **same result** — not
duplicated data. This is the single most important property of a good pipeline.

Our pipeline is idempotent by design: each stage **overwrites** its output file
(`staging.csv`, `clean.csv`) rather than appending. So if a run fails halfway and
you re-run it, you get the correct result — never doubled rows.

Why it matters:
- **Retries are safe** — Airflow can re-run a failed task and nothing breaks.
- **Re-runs are safe** — need to reprocess yesterday? Just run it again.
"""))

    # 6
    C(md("""
---
## 6. When things fail

Tutorials show the happy path. Real pipelines spend their life in the *unhappy*
path — networks drop, files arrive late, a value is missing. Airflow treats
failure as normal:

| Mechanism | What it does |
|-----------|--------------|
| **Retries** | Re-run a failed task N times, with a delay (`retries=3`) |
| **Partial re-runs** | Only the failed task re-runs — not the whole pipeline |
| **Logs** | Every task run keeps its full output — you debug from logs, not guesses |
| **Alerts** | Notify (email/Slack) on failure |

> **The 3 AM test:** *"If this fails at 3 AM on a Saturday, what happens?"* If the
> answer is "a human wakes up and runs commands in the right order and hopes" —
> that's a script with a schedule, not orchestration.
"""))

    # 7
    C(md("""
---
## 7. Airflow: DAGs & tasks in code

In Airflow you write your pipeline as a **DAG** of **tasks**. With the
**TaskFlow API**, a task is just a decorated Python function. Here's your repo's
demo DAG (`dags/demo_dag.py`):

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(schedule=None, start_date=datetime(2024, 1, 1), catchup=False)
def demo_etl():
    @task
    def extract():
        print("read the data")
    @task
    def transform():
        print("clean it")
    @task
    def load():
        print("write it out")

    extract() >> transform() >> load()   # dependencies

demo_etl()
```

- `@dag` — declares the pipeline and its settings (`schedule`, retries…).
- `@task` — each step; a plain Python function.
- The last line wires the **order**.
"""))

    # 8 — the ordering vs data-passing distinction
    C(md("""
---
## 8. Wiring tasks: ordering vs passing data

There are **two** ways to connect tasks, and they mean different things:

**a) `>>` — ordering only (no data passed):**
```python
extract() >> transform() >> load()
```
"Run extract, then transform, then load." Nothing is passed between them.

**b) call / arguments — pass data (via Airflow's XCom):**
```python
data = extract()      # extract returns a value...
transform(data)       # ...transform receives it; Airflow infers the dependency
```
Here the **return value** of `extract` is handed to `transform` (Airflow stores
it in a small store called **XCom**).

**Which should you use?**
- Use **`>>`** when steps just need an **order** and share data another way — e.g.
  they read/write **files** (our case: stages hand off through `output/*.csv`).
- Use **arguments** when a task genuinely needs the previous task's **return
  value in memory** (a number, a small table).

Our capstone pipeline is file-based, so we use **`>>`** — cleaner, and no reason
to push data through XCom.
"""))

    # 9
    C(md("""
---
## 9. What Airflow is actually running

When you run `make up` (which runs `airflow standalone`), a few pieces start up:

| Piece | Role |
|-------|------|
| **Scheduler** | Watches the DAGs, decides what should run now, hands tasks to the executor |
| **Executor** | Actually runs the task code |
| **Web server (UI)** | Where you see runs, trigger DAGs, and read logs — on port 8080 |
| **Metadata DB** | Remembers DAGs, run history, task states (a local SQLite file here) |

In production these run on separate machines; `standalone` bundles them into one
process — perfect for learning.
"""))

    # 10
    C(md("""
---
## 10. See it live 👀

Enough theory — watch it run.

**In the terminal:**
```bash
make up
```
This starts Airflow and prints an `admin` password (give it ~60–90s). Open the
**port 8080** forwarded URL (a pop-up appears, or use the **Ports** tab), log in,
then:

1. Find the **`demo_etl`** DAG and unpause it.
2. **Trigger** it (▶).
3. Watch `extract → transform → load` turn **green** in the Graph view.
4. Click a task → **Logs** to see its output.

💬 That green graph is the point: you can *see* the pipeline run, catch failures,
and schedule it. `make up` keeps that terminal busy — open a **second terminal**
for other commands.
"""))

    # 11
    C(md("""
---
## 11. Your capstone 🏗️

Now your team builds the real thing on the Superstore data — see the repo
`README.md`:

1. **Pipeline** — implement `extract/transform/load` in `src/pipeline.py`
   (`make pipeline`).
2. **Orchestrate** — wire `dags/superstore_dag.py` (`extract() >> transform() >>
   load()`), then trigger `superstore_pipeline` in the UI and watch it go green.
3. **Dashboard** — build `app.py` (`make dash`).
4. **Stretch** — give the DAG a `schedule`, add retries, richer dashboard, deploy
   to Streamlit Cloud.

Everything you need you've done across Days 1–3 — now it's yours to assemble. 🚀
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
