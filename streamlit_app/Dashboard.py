import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_mart

st.set_page_config(
    page_title="SupplySight AI",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #f5f7fb;
        }

        [data-testid="stAppViewContainer"] {
            background: #f5f7fb;
        }

        [data-testid="stHeader"] {
            background: rgba(245, 247, 251, 0.92);
        }

        .main .block-container {
            max-width: 1500px;
            padding-top: 0;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e6eaf0;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
        }

        [data-testid="stSidebar"] * {
            color: #334155;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 10px;
            margin: 3px 10px;
            padding: 8px 12px;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: #eef5ff;
            color: #1769d2;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: #eaf3ff;
            color: #1769d2;
            font-weight: 700;
        }

        h1 {
            color: #102a43;
            font-size: 2.55rem;
            font-weight: 800;
            letter-spacing: -0.8px;
            margin-bottom: 0.15rem;
        }

        h2 {
            color: #123b63;
            font-size: 1.55rem;
            font-weight: 750;
            letter-spacing: -0.2px;
            margin-top: 2.2rem;
            margin-bottom: 1rem;
        }

        h3 {
            color: #183b5c;
            font-size: 1.02rem;
            font-weight: 700;
        }

        p {
            color: #64748b;
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e7ebf1;
            border-radius: 0;
            padding: 18px 20px;
            min-height: 112px;
            box-shadow: 0 5px 18px rgba(30, 55, 90, 0.06);
        }

        [data-testid="stMetricLabel"] {
            color: #64748b;
            font-size: 0.82rem;
            font-weight: 650;
        }

        [data-testid="stMetricValue"] {
            color: #102a43;
            font-size: 1.72rem;
            font-weight: 800;
        }

        .chart-card {
            background: #ffffff;
            border: 1px solid #e7ebf1;
            border-radius: 0;
            padding: 14px 16px 8px 16px;
            margin-bottom: 18px;
            box-shadow: 0 5px 18px rgba(30, 55, 90, 0.055);
        }

        .chart-title {
            color: #183b5c;
            font-size: 1rem;
            font-weight: 750;
            margin: 2px 0 2px 4px;
        }

        .chart-subtitle {
            color: #7b8794;
            font-size: 0.76rem;
            margin: 0 0 7px 4px;
        }

        .hero {
            width: 65%;
            margin: 0 auto 30px auto;
            background: #ffffff;
            border: 1px solid #e7ebf1;
            border-radius: 0;
            padding: 42px 30px 38px 30px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(30, 55, 90, 0.035);
        }

        .hero-title {
            color: #102a43;
            font-size: 2.45rem;
            font-weight: 850;
            letter-spacing: -0.8px;
            text-align: center;
            margin: 0;
        }

        .hero-text {
            color: #62758a;
            font-size: 0.98rem;
            margin: 7px auto 0 auto;
            max-width: 760px;
            text-align: center;
        }

        [data-testid="stPlotlyChart"] {
            margin-top: -4px;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid #e7ebf1;
            border-radius: 12px;
            overflow: hidden;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


PLOT_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}


PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Inter, Arial, sans-serif",
        "color": "#52677d",
    },
    "margin": {"l": 12, "r": 12, "t": 12, "b": 12},
    "height": 320,
    "hoverlabel": {
        "bgcolor": "#102a43",
        "font": {"color": "#ffffff"},
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
        f"""
        <div class="chart-card">
            <div class="chart-title">{title}</div>
            <div class="chart-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def section(title):
    st.header(title)


sales = load_mart("Sales_Mart")
procurement = load_mart("Procurement_Mart")
inventory = load_mart("Inventory_Mart")
logistics = load_mart("Logistics_Mart")


st.markdown(
    """
    <div class="hero">
        <div class="hero-title">SupplySight AI</div>
        <div class="hero-text">
            Supply chain analytics mapping Stores, Warehouses, Sales, Shipment ,and Inventory Logistics.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


section("Sales Analytics")

return_rate = (
    sales["ReturnedQuantity"].sum() / sales["QuantitySold"].sum() * 100
    if sales["QuantitySold"].sum() != 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Net Sales",
        f"{sales['NetSalesAmount'].sum():,.0f}",
    )
with col2:
    st.metric(
        "Units Sold",
        f"{sales['QuantitySold'].sum():,.0f}",
    )
with col3:
    st.metric(
        "Transactions",
        f"{sales['SalesID'].nunique():,.0f}",
    )
with col4:
    st.metric(
        "Return Rate",
        f"{return_rate:.2f}%",
    )


sales["FullDate"] = pd.to_datetime(sales["FullDate"])

monthly_sales = (
    sales.groupby(sales["FullDate"].dt.to_period("M"))["NetSalesAmount"]
    .sum()
    .reset_index()
)
monthly_sales["FullDate"] = monthly_sales["FullDate"].astype(str)

sales_by_city = (
    sales.groupby("City")["NetSalesAmount"]
    .sum()
    .sort_values(ascending=False)
)

top_subcategories = (
    sales.groupby("SubCategory")["NetSalesAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

brand_performance = (
    sales.groupby("Brand")
    .agg(
        Sales=("NetSalesAmount", "sum"),
        QuantitySold=("QuantitySold", "sum"),
    )
    .sort_values("Sales", ascending=False)
    .head(10)
)


col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        monthly_sales,
        x="FullDate",
        y="NetSalesAmount",
        markers=True,
    )

    fig.update_traces(line_width=3)

    chart_card(
        "Monthly Sales",
        "Net sales trend over time",
        clean_fig(fig),
    )

with col2:
    city_df = sales_by_city.reset_index()
    city_df.columns = ["City", "NetSalesAmount"]

    fig = px.bar(
        city_df,
        x="City",
        y="NetSalesAmount",
    )

    chart_card(
        "Sales by City",
        "Net sales contribution by city",
        clean_fig(fig),
    )


col1, col2 = st.columns(2)

with col1:
    sub_df = top_subcategories.reset_index()
    sub_df.columns = ["SubCategory", "NetSalesAmount"]

    fig = px.bar(
        sub_df,
        x="NetSalesAmount",
        y="SubCategory",
        orientation="h",
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    chart_card(
        "Top SubCategories",
        "Top 10 subcategories by net sales",
        clean_fig(fig),
    )

with col2:
    brand_df = brand_performance.reset_index()

    fig = go.Figure()

    fig.add_bar(
        x=brand_df["Brand"],
        y=brand_df["Sales"],
        name="Sales",
    )

    fig.add_bar(
        x=brand_df["Brand"],
        y=brand_df["QuantitySold"],
        name="Quantity Sold",
    )

    fig.update_layout(barmode="group")

    chart_card(
        "Brand Popularity and Performance",
        "Sales value compared with quantity sold",
        clean_fig(fig),
    )


section("Procurement Analytics")


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Procurement Spend",
        f"{procurement['TotalItemCost'].sum():,.0f}",
    )
with col2:
    st.metric(
        "Purchase Orders",
        f"{procurement['PurchaseOrderID'].nunique():,.0f}",
    )
with col3:
    st.metric(
        "Suppliers",
        f"{procurement['SupplierID'].nunique():,.0f}",
    )
with col4:
    st.metric(
        "Average Lead Time",
        f"{procurement['LeadTimeDays'].mean():.1f} days",
    )


supplier_rating_defect = (
    procurement.groupby(["SupplierName", "SupplierRating"])
    ["DefectRatePercentage"]
    .mean()
    .reset_index()
)

size_defect = (
    procurement.groupby("SupplierSize")["DefectRatePercentage"]
    .mean()
    .sort_values(ascending=False)
)

quantity_by_category = (
    procurement.groupby("Category")["QuantityOrdered"]
    .sum()
    .sort_values(ascending=False)
)

tier_defect = (
    procurement.groupby("SupplierTier")["DefectRatePercentage"]
    .mean()
    .sort_values(ascending=False)
)


col1, col2 = st.columns(2)
with col1:
    fig = px.scatter(
        supplier_rating_defect,
        x="SupplierRating",
        y="DefectRatePercentage",
        hover_name="SupplierName",
        size="DefectRatePercentage",
    )

    chart_card(
        "Supplier Rating vs Defect Rate",
        "Relationship between supplier rating and average defect rate",
        clean_fig(fig),
    )

with col2:
    size_df = size_defect.reset_index()
    size_df.columns = ["SupplierSize", "DefectRatePercentage"]

    fig = px.bar(
        size_df,
        x="SupplierSize",
        y="DefectRatePercentage",
    )

    chart_card(
        "Supplier Size vs Defect Rate",
        "Average defect rate across supplier sizes",
        clean_fig(fig),
    )


col1, col2 = st.columns(2)
with col1:
    category_df = quantity_by_category.reset_index()
    category_df.columns = ["Category", "QuantityOrdered"]

    fig = px.bar(
        category_df,
        x="Category",
        y="QuantityOrdered",
    )

    chart_card(
        "Quantity Procured by Category",
        "Total quantity ordered across product categories",
        clean_fig(fig),
    )

with col2:
    tier_df = tier_defect.reset_index()
    tier_df.columns = ["SupplierTier", "DefectRatePercentage"]

    fig = px.bar(
        tier_df,
        x="SupplierTier",
        y="DefectRatePercentage",
    )

    chart_card(
        "Supplier Tier vs Defect Rate",
        "Average defect rate by supplier tier",
        clean_fig(fig),
    )


section("Inventory Analytics")

below_reorder = (
    inventory["AvailableStock"] < inventory["ReorderLevel"]
).sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Current Stock",
        f"{inventory['CurrentStock'].sum():,.0f}",
    )
with col2:
    st.metric(
        "Reserved Stock",
        f"{inventory['ReservedStock'].sum():,.0f}",
    )
with col3:
    st.metric(
        "Available Stock",
        f"{inventory['AvailableStock'].sum():,.0f}",
    )
with col4:
    st.metric(
        "Below Reorder Level",
        f"{below_reorder:,.0f}",
    )


warehouse_by_state = (
    inventory.groupby("State")["WarehouseID"]
    .nunique()
    .sort_values(ascending=False)
)

inventory_by_category = (
    inventory.groupby("Category")["CurrentStock"]
    .sum()
    .sort_values(ascending=False)
)

inventory_condition = inventory["InventoryCondition"].value_counts()

stock_reorder = (
    inventory.groupby("Category")[["AvailableStock", "ReorderLevel"]]
    .sum()
    .sort_values("AvailableStock", ascending=False)
)

col1, col2 = st.columns(2)
with col1:
    warehouse_df = warehouse_by_state.reset_index()
    warehouse_df.columns = ["State", "WarehouseID"]

    fig = px.bar(
        warehouse_df,
        x="State",
        y="WarehouseID",
    )

    chart_card(
        "Warehouse Distribution by State",
        "Number of warehouses by state",
        clean_fig(fig),
    )

with col2:
    inventory_category_df = inventory_by_category.reset_index()
    inventory_category_df.columns = ["Category", "CurrentStock"]

    fig = px.bar(
        inventory_category_df,
        x="Category",
        y="CurrentStock",
    )

    chart_card(
        "Inventory by Category",
        "Current stock across product categories",
        clean_fig(fig),
    )


col1, col2 = st.columns(2)
with col1:
    condition_df = inventory_condition.reset_index()
    condition_df.columns = ["InventoryCondition", "Count"]

    fig = px.bar(
        condition_df,
        x="InventoryCondition",
        y="Count",
    )

    chart_card(
        "Inventory Condition",
        "Inventory records by condition",
        clean_fig(fig),
    )

with col2:
    stock_df = stock_reorder.reset_index()

    fig = go.Figure()

    fig.add_bar(
        x=stock_df["Category"],
        y=stock_df["AvailableStock"],
        name="Available Stock",
    )

    fig.add_bar(
        x=stock_df["Category"],
        y=stock_df["ReorderLevel"],
        name="Reorder Level",
    )

    fig.update_layout(barmode="group")

    chart_card(
        "Available Stock vs Reorder Level",
        "Current availability compared with reorder requirements",
        clean_fig(fig),
    )


section("Logistics Analytics")

on_time_rate = logistics["OnTimeFlag"].mean() * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Shipments",
        f"{logistics['ShipmentID'].nunique():,.0f}",
    )
with col2:
    st.metric(
        "On-Time Rate",
        f"{on_time_rate:.2f}%",
    )
with col3:
    st.metric(
        "Average Delay",
        f"{logistics['DelayDays'].mean():.2f} days",
    )
with col4:
    st.metric(
        "Freight Cost",
        f"{logistics['FreightCost'].sum():,.0f}",
    )

delay_distribution = (
    logistics["DelayDays"]
    .value_counts()
    .sort_index()
)

weather_delay = (
    logistics[
        logistics["WeatherSeverity"].notna()
        & ~logistics["WeatherSeverity"]
        .astype(str)
        .str.strip()
        .isin(["\\N", "/N", "N/A", "NA", "NULL", "None", ""])
    ]
    .groupby("WeatherSeverity")["DelayDays"]
    .mean()
    .sort_values(ascending=False)
)

transport_delay = (
    logistics.groupby("TransportMode")["DelayDays"]
    .mean()
    .sort_values(ascending=False)
)

freight_distance = logistics[
    ["DistanceKM", "FreightCost"]
].dropna()


col1, col2 = st.columns(2)
with col1:
    delay_df = delay_distribution.reset_index()
    delay_df.columns = ["DelayDays", "ShipmentCount"]

    fig = px.bar(
        delay_df,
        x="DelayDays",
        y="ShipmentCount",
    )

    chart_card(
        "Delay Distribution",
        "Shipment count by number of delay days",
        clean_fig(fig),
    )

with col2:
    weather_df = weather_delay.reset_index()
    weather_df.columns = ["WeatherSeverity", "DelayDays"]

    fig = px.bar(
        weather_df,
        x="WeatherSeverity",
        y="DelayDays",
    )

    chart_card(
        "Weather Severity vs Delay",
        "Average delay associated with weather severity",
        clean_fig(fig),
    )


col1, col2 = st.columns(2)
with col1:
    transport_df = transport_delay.reset_index()
    transport_df.columns = ["TransportMode", "DelayDays"]

    fig = px.bar(
        transport_df,
        x="TransportMode",
        y="DelayDays",
    )

    chart_card(
        "Transport Mode vs Delay",
        "Average delay by transportation mode",
        clean_fig(fig),
    )

with col2:
    fig = px.scatter(
        freight_distance,
        x="DistanceKM",
        y="FreightCost",
    )

    chart_card(
        "Freight Cost vs Distance",
        "Relationship between shipment distance and freight cost",
        clean_fig(fig),
    )


st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        font-size:0.75rem;
        padding:28px 0 8px 0;
    ">
        SupplySight AI · Supply Chain Analytics
    </div>
    """,
    unsafe_allow_html=True,
)
