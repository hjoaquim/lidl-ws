"""Airflow DAG that orchestrates the Superstore pipeline.

Same three stages as src/pipeline.py, but now as Airflow **tasks** that run in
order — so you get scheduling, retries, and the UI for free.

    extract  ->  transform  ->  load
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from airflow.decorators import dag, task

# make the `src` package importable no matter where Airflow runs the task
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@dag(
    dag_id="superstore_pipeline",
    description="Extract -> transform -> load the Superstore data.",
    schedule=None,           # trigger manually from the UI (or set e.g. "@daily")
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["capstone"],
)
def superstore_pipeline():

    @task
    def extract() -> int:
        from src.pipeline import extract
        return extract()

    @task
    def transform(_rows: int) -> int:
        from src.pipeline import transform
        return transform()

    @task
    def load(_rows: int) -> str:
        from src.pipeline import load
        return load()

    load(transform(extract()))


superstore_pipeline()
