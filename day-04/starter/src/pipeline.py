"""Superstore data pipeline: extract -> transform -> load.

Fill in the three stages, then run the whole thing:

    python -m src.pipeline

Each stage reads/writes files under output/, so the same functions can run from
the command line AND as Airflow tasks. Paths are resolved relative to the repo
root — don't change ROOT / RAW / OUT.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "Sample - Superstore.csv"
OUT = ROOT / "output"


def extract() -> int:
    """EXTRACT: read the raw CSV (encoding='latin-1') and save it to
    output/staging.csv. Return the number of rows.
    Hint: OUT.mkdir(exist_ok=True) before writing."""
    raise NotImplementedError("Implement extract()")


def transform() -> int:
    """TRANSFORM: read output/staging.csv, clean it (snake_case columns, parse the
    two date columns, drop row_id/country, drop duplicates and empty rows, fix
    postal_code), and write output/clean.csv. Return the row count.
    You did every one of these steps on Day 2."""
    raise NotImplementedError("Implement transform()")


def load() -> str:
    """LOAD: read output/clean.csv and write the summary tables the dashboard
    reads — e.g. output/summary_region.csv (sales + profit per region).
    Return 'output/'."""
    raise NotImplementedError("Implement load()")


def run_all() -> None:
    extract()
    transform()
    load()
    print("✅ pipeline complete")


if __name__ == "__main__":
    run_all()
