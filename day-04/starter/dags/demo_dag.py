"""A tiny demo DAG for the teaching block: extract -> transform -> load.

Trivial tasks (no real data) so it always runs — the point is to *see*
orchestration: tasks, their dependencies, and a run going green in the UI.
"""
from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag, task


@dag(dag_id="demo_etl", schedule=None, start_date=datetime(2024, 1, 1),
     catchup=False, tags=["demo"])
def demo_etl():

    @task
    def extract() -> int:
        print("Pretend we read 100 rows from a source.")
        return 100

    @task
    def transform(rows: int) -> int:
        cleaned = rows - 3
        print(f"Cleaning {rows} rows -> {cleaned} after dropping dupes.")
        return cleaned

    @task
    def load(rows: int) -> None:
        print(f"Loaded {rows} clean rows to the warehouse. ✅")

    load(transform(extract()))


demo_etl()
