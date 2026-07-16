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
    def extract():
        print("Extract: read 100 rows from the source.")

    @task
    def transform():
        print("Transform: cleaned the rows (dropped duplicates).")

    @task
    def load():
        print("Load: wrote the clean rows to the warehouse. ✅")

    # '>>' sets the order: run extract, then transform, then load.
    extract() >> transform() >> load()


demo_etl()
