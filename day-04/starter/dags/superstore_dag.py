"""Wrap your pipeline in an Airflow DAG: extract -> transform -> load.

Fill in each task so it calls the matching function from src.pipeline, then wire
the tasks in order. Once it's right it appears in the Airflow UI and you can
trigger it. (The demo_dag.py next to this file is a complete example to copy from.)
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from airflow.decorators import dag, task

# make the `src` package importable no matter where Airflow runs the task
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@dag(dag_id="superstore_pipeline", schedule=None,
     start_date=datetime(2024, 1, 1), catchup=False, tags=["capstone"])
def superstore_pipeline():

    @task
    def extract():
        # TODO: call extract() from src.pipeline
        raise NotImplementedError

    @task
    def transform():
        # TODO: call transform() from src.pipeline
        raise NotImplementedError

    @task
    def load():
        # TODO: call load() from src.pipeline
        raise NotImplementedError

    # TODO: wire the tasks so they run in order, e.g. extract() >> transform() >> load()
    ...


superstore_pipeline()
