"""Superstore dashboard. Fill in the TODOs, then run:

    streamlit run app.py

(You built one of these on Day 3 — reuse that knowledge.)
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Superstore Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(ROOT / "output" / "clean.csv", parse_dates=["order_date", "ship_date"])


st.title("📊 Superstore Sales Dashboard")
st.info("Build me! Run the pipeline first (`make pipeline`), then fill in the TODOs in app.py.")

# TODO: load the data with load_data(); show a friendly message if output/clean.csv is missing
# TODO: a sidebar region filter (st.multiselect) and filter the DataFrame
# TODO: a KPI row (st.columns + st.metric): total sales, total profit, orders
# TODO: at least one chart, e.g. st.plotly_chart(px.bar(... sales by region ...))
