"""Superstore sales dashboard (Streamlit).

Run it:

    streamlit run src/app.py

In Codespaces a pop-up offers to open the forwarded port — click it.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Superstore Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    # find data/clean.csv whether run from the repo root or src/
    path = next(
        p
        for p in [Path("day-03/starter/data/clean.csv"), Path("../data/clean.csv")]
        if p.exists()
    )
    return pd.read_csv(path, parse_dates=["order_date", "ship_date"])


df = load_data()

st.title("📊 Superstore Sales Dashboard")
st.caption("Sales & profitability across regions, categories, customers and time.")

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")

regions = sorted(df["region"].unique())
categories = sorted(df["category"].unique())
segments = sorted(df["segment"].unique())

chosen_regions = st.sidebar.multiselect("Region", regions, default=regions)
chosen_categories = st.sidebar.multiselect("Category", categories, default=categories)
chosen_segments = st.sidebar.multiselect("Segment", segments, default=segments)

min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
date_range = st.sidebar.date_input(
    "Order date range", (min_date, max_date), min_value=min_date, max_value=max_date
)
# date_input returns a single date until both ends are picked
start, end = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else (min_date, max_date)

view = df[
    df["region"].isin(chosen_regions)
    & df["category"].isin(chosen_categories)
    & df["segment"].isin(chosen_segments)
    & df["order_date"].dt.date.between(start, end)
]

if view.empty:
    st.warning("No data for the current filters — widen them in the sidebar.")
    st.stop()

# ---------------- KPI row ----------------
sales = view["sales"].sum()
profit = view["profit"].sum()
margin = profit / sales if sales else 0

# vs. the full (unfiltered) dataset, so KPIs show how the selection compares
full_margin = df["profit"].sum() / df["sales"].sum()

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total sales", f"${sales:,.0f}")
c2.metric("Total profit", f"${profit:,.0f}")
c3.metric("Profit margin", f"{margin:.1%}", delta=f"{margin - full_margin:+.1%} vs all")
c4.metric("Orders", f"{view['order_id'].nunique():,}", help="Unique orders, not line items")
c5.metric("Customers", f"{view['customer_id'].nunique():,}")
c6.metric("Avg discount", f"{view['discount'].mean():.0%}")

tab_trend, tab_breakdown, tab_profit, tab_rank, tab_geo = st.tabs(
    ["📈 Trends", "🧩 Breakdowns", "💸 Profitability", "🏆 Rankings", "🗺️ Geography"]
)

# ---------------- Trends ----------------
with tab_trend:
    metric = st.radio("Metric", ["sales", "profit"], horizontal=True, key="trend_metric")
    monthly = (
        view.groupby(view["order_date"].dt.to_period("M").dt.to_timestamp())[metric]
        .sum()
        .reset_index()
    )
    st.plotly_chart(
        px.line(monthly, x="order_date", y=metric, markers=True, title=f"Monthly {metric}"),
        use_container_width=True,
    )

    # year-over-year: same months stacked across years
    yoy = view.copy()
    yoy["year"] = yoy["order_date"].dt.year
    yoy["month"] = yoy["order_date"].dt.month
    yoy = yoy.groupby(["year", "month"])[metric].sum().reset_index()
    yoy["year"] = yoy["year"].astype(str)
    st.plotly_chart(
        px.line(yoy, x="month", y=metric, color="year", markers=True,
                title=f"{metric.title()} by month, year over year"),
        use_container_width=True,
    )

# ---------------- Breakdowns ----------------
with tab_breakdown:
    left, right = st.columns(2)
    by_region = view.groupby("region")["sales"].sum().sort_values().reset_index()
    left.plotly_chart(
        px.bar(by_region, x="sales", y="region", orientation="h", title="Sales by region"),
        use_container_width=True,
    )
    by_cat = view.groupby("category")["sales"].sum().reset_index()
    right.plotly_chart(
        px.pie(by_cat, names="category", values="sales", title="Sales share by category", hole=0.4),
        use_container_width=True,
    )

    seg = view.groupby(["segment", "category"])["sales"].sum().reset_index()
    st.plotly_chart(
        px.bar(seg, x="segment", y="sales", color="category", barmode="group",
               title="Sales by segment and category"),
        use_container_width=True,
    )

    st.subheader("Sales heatmap — region × category")
    pivot = view.pivot_table(values="sales", index="region", columns="category", aggfunc="sum", fill_value=0)
    st.plotly_chart(
        px.imshow(pivot, text_auto=".0f", aspect="auto", color_continuous_scale="Blues"),
        use_container_width=True,
    )

# ---------------- Profitability ----------------
with tab_profit:
    st.subheader("Profit by sub-category — the money losers")
    by_sub = view.groupby("sub_category")["profit"].sum().sort_values().reset_index()
    by_sub["sign"] = (by_sub["profit"] >= 0).map({True: "profit", False: "loss"})
    st.plotly_chart(
        px.bar(by_sub, x="profit", y="sub_category", orientation="h", color="sign",
               color_discrete_map={"profit": "seagreen", "loss": "tomato"},
               title="Total profit by sub-category"),
        use_container_width=True,
    )

    st.subheader("Discount vs profit — high discounts bleed money")
    sample = view.sample(min(1500, len(view)), random_state=0)
    st.plotly_chart(
        px.scatter(sample, x="discount", y="profit", color="category",
                   hover_data=["product_name"], opacity=0.6, title="Discount vs profit"),
        use_container_width=True,
    )

    st.subheader("Margin by category")
    cat = view.groupby("category").agg(sales=("sales", "sum"), profit=("profit", "sum")).reset_index()
    cat["margin"] = cat["profit"] / cat["sales"]
    st.plotly_chart(
        px.bar(cat, x="category", y="margin", color="margin", text_auto=".1%",
               color_continuous_scale="RdYlGn", title="Profit margin by category"),
        use_container_width=True,
    )

# ---------------- Rankings ----------------
with tab_rank:
    n = st.slider("How many to show", 5, 25, 10)
    left, right = st.columns(2)

    top_products = (
        view.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(n).reset_index()
    )
    left.plotly_chart(
        px.bar(top_products, x="sales", y="product_name", orientation="h",
               title=f"Top {n} products by sales").update_yaxes(autorange="reversed"),
        use_container_width=True,
    )

    top_customers = (
        view.groupby("customer_name")["profit"].sum().sort_values(ascending=False).head(n).reset_index()
    )
    right.plotly_chart(
        px.bar(top_customers, x="profit", y="customer_name", orientation="h",
               title=f"Top {n} customers by profit").update_yaxes(autorange="reversed"),
        use_container_width=True,
    )

    st.subheader("Ship mode mix")
    ship = view.groupby("ship_mode").agg(orders=("order_id", "nunique"), sales=("sales", "sum")).reset_index()
    st.plotly_chart(
        px.bar(ship, x="ship_mode", y="orders", title="Orders by ship mode"),
        use_container_width=True,
    )

# ---------------- Geography ----------------
with tab_geo:
    by_state = view.groupby("state").agg(
        sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")
    ).reset_index().sort_values("sales", ascending=False)

    st.plotly_chart(
        px.bar(by_state.head(15), x="state", y="sales", title="Top 15 states by sales"),
        use_container_width=True,
    )
    st.subheader("State detail")
    st.dataframe(
        by_state.style.format({"sales": "${:,.0f}", "profit": "${:,.0f}", "orders": "{:,}"}),
        use_container_width=True,
    )

st.caption(f"Showing {len(view):,} of {len(df):,} line items after filters.")
