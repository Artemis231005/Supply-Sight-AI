import streamlit as st
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_percentage_error,
    mean_absolute_error,
    mean_squared_error,
)

import plotly.express as px
from utils import load_mart


st.set_page_config(
    page_title="Sales Forecasting",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: #f5f7fb
        }

        [data-testid="stHeader"] {
            background: rgba(245,247,251,.92)
        }

        .main .block-container {
            max-width: 1500px;
            padding-top: 0;
            padding-bottom: 3rem
        }

        [data-testid="stSidebar"] {
            background: #fff;
            border-right: 1px solid #e6eaf0
        }

        [data-testid="stSidebar"] * {
            color: #334155
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 10px;
            margin: 3px 10px;
            padding: 8px 12px
        }

        [data-testid="stSidebarNav"] a:hover {
            background: #eef5ff;
            color: #1769d2
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: #eaf3ff;
            color: #1769d2;
            font-weight: 700
        }

        h1 {
            color: #102a43;
            font-size: 2.55rem;
            font-weight: 800
        }

        h2 {
            color: #123b63;
            font-size: 1.55rem;
            font-weight: 750;
            margin-top: 2.2rem
        }

        h3 {
            color: #183b5c
        }

        p, label {
            color: #64748b
        }

        [data-testid="stMetric"] {
            background: #fff;
            border: 1px solid #e7ebf1;
            border-radius: 0;
            padding: 18px 20px;
            min-height: 112px;
            box-shadow: 0 5px 18px rgba(30,55,90,.06)
        }

        [data-testid="stMetricLabel"] {
            color: #64748b;
            font-size: .82rem;
            font-weight: 650
        }

        [data-testid="stMetricValue"] {
            color: #102a43;
            font-size: 1.72rem;
            font-weight: 800
        }

        .hero {
            width: 70%;
            margin: 0 auto 30px auto;
            background: #fff;
            border: 1px solid #e7ebf1;
            border-radius: 0;
            padding: 42px 30px 38px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(30,55,90,.035)
        }

        .hero-title {
            color: #102a43;
            font-size: 2.45rem;
            font-weight: 850;
            letter-spacing: -.8px;
            text-align: center;
            margin: 0
        }

        .hero-text {
            color: #62758a;
            font-size: .98rem;
            margin: 7px auto 0;
            max-width: 760px;
            text-align: center
        }

        .chart-card, .table-card {
            background: #fff;
            border: 1px solid #e7ebf1;
            border-radius: 0;
            padding: 14px 16px 8px;
            margin-bottom: 18px;
            box-shadow: 0 5px 18px rgba(30,55,90,.055)
        }

        .table-card {
            padding-bottom: 16px
        }

        .chart-title {
            color: #183b5c;
            font-size: 1rem;
            font-weight: 750;
            margin: 2px 0 2px 4px
        }

        .chart-subtitle {
            color: #7b8794;
            font-size: .76rem;
            margin: 0 0 7px 4px
        }

        [data-testid="stPlotlyChart"] {
            margin-top: -4px
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #e7ebf1;
            border-radius: 0;
            overflow: hidden
        }

        #MainMenu, footer {
            visibility: hidden
        }
    </style>
    """,
    unsafe_allow_html=True
)


PLOT_CONFIG = {"displayModeBar": False, "responsive": True}

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Inter,Arial,sans-serif",
        "color": "#52677d"
    },
    "margin": {
        "l": 12,
        "r": 12,
        "t": 12,
        "b": 12
    },
    "height": 320,
    "hoverlabel": {
        "bgcolor": "#102a43",
        "font": {
            "color": "#fff"
        }
    },
}


def clean_fig(fig):
    fig.update_layout(**PLOTLY_LAYOUT)

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#e7ebf1",
        tickfont={"size": 11, "color": "#718096"},
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#edf1f5",
        zeroline=False,
        linecolor="#e7ebf1",
        tickfont={"size": 11, "color": "#718096"},
    )

    return fig


def chart_card(title, subtitle, fig):
    st.markdown(
        f'<div class="chart-card"><div class="chart-title">{title}</div>'
        f'<div class="chart-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="hero-title">{title}</div>'
        f'<div class="hero-text">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def table_card(title, subtitle):
    st.markdown(
        f'<div class="table-card"><div class="chart-title">{title}</div>'
        f'<div class="chart-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


hero(
    "Sales Forecasting",
    "Sales forecasting using historical Sales Patterns and Naive baseline model",
)


sales = load_mart("Sales_Mart")
sales["FullDate"] = pd.to_datetime(sales["FullDate"])


daily_sales = (
    sales.groupby("FullDate")
    .agg(
        NetSales=("NetSalesAmount", "sum"),
        QuantitySold=("QuantitySold", "sum"),
    )
    .reset_index()
    .sort_values("FullDate")
)


st.header("Historical Sales")

fig = px.line(
    daily_sales,
    x="FullDate",
    y="NetSales",
)

fig.update_traces(line_width=3)

chart_card(
    "Historical Sales",
    "Daily net sales performance across the available historical period",
    clean_fig(fig),
)


st.header("Sales Forecast")


st.markdown(
    """
    <div class="chart-card">
        <div class="chart-title">Forecast Controls</div>
        <div class="chart-subtitle">
            Choose the forecast horizon and use the latest observed sales value as the Naive baseline.
        </div>
    """,
    unsafe_allow_html=True,
)


control_col1, control_col2 = st.columns(2)


with control_col1:
    forecast_days = st.slider(
        "Forecast Horizon (days)",
        min_value=7,
        max_value=60,
        value=30,
        step=1,
    )


with control_col2:
    baseline_window = st.selectbox(
        "Baseline",
        ["Latest Day (Naive)", "Average of Last 7 Days"],
        index=0,
    )


st.markdown("</div>", unsafe_allow_html=True)


forecast_data = daily_sales.copy()
forecast_data["Lag_1"] = forecast_data["NetSales"].shift(1)
forecast_data = forecast_data.dropna().reset_index(drop=True)


split = int(len(forecast_data) * 0.80)


if len(forecast_data) >= 10 and split < len(forecast_data):
    train_sales = forecast_data.iloc[:split]
    test_sales = forecast_data.iloc[split:]

    y_test_sales = test_sales["NetSales"]
    sales_naive_pred = test_sales["Lag_1"]

    naive_mape = mean_absolute_percentage_error(
        y_test_sales,
        sales_naive_pred,
    )

    naive_mae = mean_absolute_error(
        y_test_sales,
        sales_naive_pred,
    )

    naive_rmse = np.sqrt(
        mean_squared_error(
            y_test_sales,
            sales_naive_pred,
        )
    )

else:
    naive_mape = np.nan
    naive_mae = np.nan
    naive_rmse = np.nan


if baseline_window == "Latest Day (Naive)":
    future_value = daily_sales["NetSales"].iloc[-1]

else:
    future_value = daily_sales["NetSales"].tail(7).mean()


future_dates = pd.date_range(
    daily_sales["FullDate"].max() + pd.Timedelta(days=1),
    periods=forecast_days,
)


predictions = np.repeat(future_value, forecast_days)

forecast = pd.DataFrame(
    {
        "Date": future_dates,
        "Forecast": predictions,
    }
)


historical_plot = daily_sales.tail(90).copy()


fig = px.line(
    historical_plot,
    x="FullDate",
    y="NetSales",
)


fig.update_traces(
    name="Historical",
    line_width=3,
)


fig.add_scatter(
    x=forecast["Date"],
    y=forecast["Forecast"],
    mode="lines",
    name="Forecast",
    line=dict(width=3, dash="dash"),
)


fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)


chart_card(
    "Historical vs Forecast Sales",
    f"Last 90 historical days followed by the selected {forecast_days}-day forecast",
    clean_fig(fig),
)


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Forecast Sales",
        f"₹{forecast['Forecast'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Average Daily Forecast",
        f"₹{forecast['Forecast'].mean():,.0f}"
    )


st.header("Sales Trend Analysis")

monthly_sales = (
    sales.assign(
        Month=sales["FullDate"].dt.to_period("M").astype(str)
    )
    .groupby("Month")
    .agg(
        NetSales=("NetSalesAmount", "sum"),
        UnitsSold=("QuantitySold", "sum"),
    )
    .reset_index()
)


fig = px.line(
    monthly_sales,
    x="Month",
    y="NetSales",
    markers=True,
)


chart_card(
    "Monthly Sales Trend",
    "Monthly net sales used to identify longer-term changes in sales performance",
    clean_fig(fig),
)


st.header("Sales by Category")


category_sales = (
    sales.groupby("Category")
    .agg(
        NetSales=("NetSalesAmount", "sum"),
        UnitsSold=("QuantitySold", "sum"),
    )
    .sort_values("NetSales", ascending=False)
    .reset_index()
)


fig = px.bar(
    category_sales,
    x="Category",
    y="NetSales",
)


chart_card(
    "Sales by Category",
    "Net sales generated by each product category",
    clean_fig(fig),
)


table_card(
    "Category Sales Detail",
    "Net sales and units sold by category",
)


st.dataframe(
    category_sales.set_index("Category").round(2),
    use_container_width=True,
)


st.markdown("</div>", unsafe_allow_html=True)

