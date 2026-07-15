"""Superstore data pipeline: extract -> transform -> load.

Run the whole thing:

    python -m src.pipeline      (or: python src/pipeline.py)

Each stage reads/writes files under output/, so the same functions work when
called from the command line *and* as Airflow tasks. Paths are resolved
relative to the repo root, so it doesn't matter what folder you run it from.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "Sample - Superstore.csv"
OUT = ROOT / "output"


def extract() -> int:
    """EXTRACT: read the raw CSV and land it in output/staging.csv."""
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(RAW, encoding="latin-1")  # file is Windows-encoded
    df.to_csv(OUT / "staging.csv", index=False)
    print(f"extract: {len(df)} rows -> output/staging.csv")
    return len(df)


def transform() -> int:
    """TRANSFORM: clean the landed data and write output/clean.csv."""
    df = pd.read_csv(OUT / "staging.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")
    df = df.drop(columns=["row_id", "country"], errors="ignore")
    df = df.drop_duplicates().dropna(subset=["sales"])
    df["postal_code"] = df["postal_code"].fillna(0).astype(int)
    df.to_csv(OUT / "clean.csv", index=False)
    print(f"transform: {len(df)} clean rows -> output/clean.csv")
    return len(df)


def load() -> str:
    """LOAD: build the summary tables the dashboard reads."""
    df = pd.read_csv(OUT / "clean.csv", parse_dates=["order_date", "ship_date"])
    df.groupby("region")[["sales", "profit"]].sum().to_csv(OUT / "summary_region.csv")
    (df.groupby("category")["sales"].sum().sort_values(ascending=False)
       .to_csv(OUT / "summary_category.csv"))
    print("load: wrote output/summary_region.csv, output/summary_category.csv")
    return "output/"


def run_all() -> None:
    extract()
    transform()
    load()
    print("✅ pipeline complete")


if __name__ == "__main__":
    run_all()
