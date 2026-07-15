"""Superstore dashboard — reads the pipeline's output (output/clean.csv)."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Superstore Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(ROOT / "output" / "clean.csv", parse_dates=["order_date", "ship_date"])


try:
    df = load_data()
except FileNotFoundError:
    st.error("No data yet — run the pipeline first: `python -m src.pipeline` (or trigger the DAG).")
    st.stop()

st.title("📊 Superstore Sales Dashboard")

chosen = st.sidebar.multiselect("Region", sorted(df["region"].unique()),
                                default=sorted(df["region"].unique()))
view = df[df["region"].isin(chosen)]
if view.empty:
    st.warning("Pick at least one region.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Total sales", f"${view['sales'].sum():,.0f}")
c2.metric("Total profit", f"${view['profit'].sum():,.0f}")
c3.metric("Orders", f"{view['order_id'].nunique():,}")

st.plotly_chart(px.bar(view.groupby("region")["sales"].sum().reset_index(),
                       x="region", y="sales", title="Sales by region"),
                use_container_width=True)
