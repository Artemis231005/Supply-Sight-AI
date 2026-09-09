import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
from utils import load_mart

st.set_page_config(
    page_title="Supplier Clustering",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
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

PLOT_CONFIG = {
    "displayModeBar": False,
    "responsive": True
}

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Inter,Arial,sans-serif",
        "color": "#52677d"
    },
    "margin": {"l": 12, "r": 12, "t": 12, "b": 12},
    "height": 320,
    "hoverlabel": {
        "bgcolor": "#102a43",
        "font": {"color": "#fff"}
    }
}


def clean_fig(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#e7ebf1",
        tickfont={"size": 11, "color": "#718096"}
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#edf1f5",
        zeroline=False,
        linecolor="#e7ebf1",
        tickfont={"size": 11, "color": "#718096"}
    )
    return fig


def chart_card(title, subtitle, fig):
    st.markdown(
        f'<div class="chart-card"><div class="chart-title">{title}</div>'
        f'<div class="chart-subtitle">{subtitle}</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG
    )
    st.markdown("</div>", unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="hero-title">{title}</div>'
        f'<div class="hero-text">{subtitle}</div></div>',
        unsafe_allow_html=True
    )


def table_card(title, subtitle):
    st.markdown(
        f'<div class="table-card"><div class="chart-title">{title}</div>'
        f'<div class="chart-subtitle">{subtitle}</div>',
        unsafe_allow_html=True
    )


hero(
    "Supplier Clustering",
    "Supplier segmentation based on Purchasing Volume, Quality, Lead Time, Cost, and Operational Performance."
)

procurement = load_mart("Procurement_Mart")

supplier_data = (
    procurement.groupby(["SupplierID", "SupplierName"])
    .agg(
        QuantityOrdered=("QuantityOrdered", "sum"),
        ReceivedQuantity=("ReceivedQuantity", "sum"),
        AcceptedQuantity=("AcceptedQuantity", "sum"),
        TotalItemCost=("TotalItemCost", "sum"),
        SupplierRating=("SupplierRating", "mean"),
        LeadTimeDays=("LeadTimeDays", "mean"),
        DefectRatePercentage=("DefectRatePercentage", "mean"),
        ReceiptRate=("ReceiptRate", "mean"),
        AcceptanceRate=("AcceptanceRate", "mean")
    )
    .reset_index()
)

st.header("Supplier Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Suppliers", f"{len(supplier_data):,}")

with col2:
    st.metric(
        "Average Rating",
        f"{supplier_data['SupplierRating'].mean():.2f}"
    )

with col3:
    st.metric(
        "Average Lead Time",
        f"{supplier_data['LeadTimeDays'].mean():.1f} days"
    )

features = [
    "QuantityOrdered",
    "ReceivedQuantity",
    "AcceptedQuantity",
    "TotalItemCost",
    "SupplierRating",
    "LeadTimeDays",
    "DefectRatePercentage",
    "ReceiptRate",
    "AcceptanceRate"
]

X = supplier_data[features]
X_scaled = StandardScaler().fit_transform(X)

n_clusters = 2 if len(supplier_data) >= 2 else 1

kmeans = KMeans(
    n_clusters=n_clusters,
    random_state=42,
    n_init=10
)

supplier_data["Cluster"] = kmeans.fit_predict(X_scaled)


st.header("Cluster Summary")

cluster_summary = (
    supplier_data.groupby("Cluster")
    .agg(
        Suppliers=("SupplierID", "count"),
        AverageRating=("SupplierRating", "mean"),
        AverageLeadTime=("LeadTimeDays", "mean"),
        AverageDefectRate=("DefectRatePercentage", "mean"),
        AverageReceiptRate=("ReceiptRate", "mean"),
        AverageAcceptanceRate=("AcceptanceRate", "mean"),
        TotalSpend=("TotalItemCost", "sum")
    )
)

table_card(
    "Cluster Summary",
    "Average operating characteristics for each supplier cluster"
)

st.dataframe(
    cluster_summary.round(2),
    use_container_width=True
)


st.markdown("</div>", unsafe_allow_html=True)

st.header("Supplier Clusters")

chart_data = supplier_data[
    ["SupplierName", "SupplierRating", "TotalItemCost", "Cluster"]
].copy()

chart_data["Cluster"] = "Cluster " + chart_data["Cluster"].astype(str)

fig = px.scatter(
    chart_data,
    x="SupplierRating",
    y="TotalItemCost",
    color="Cluster",
    hover_name="SupplierName"
)

chart_card(
    "Supplier Clusters",
    "Supplier segmentation by rating and total procurement spend",
    clean_fig(fig)
)

st.header("Supplier Details")

details = supplier_data[
    [
        "SupplierID",
        "SupplierName",
        "SupplierRating",
        "LeadTimeDays",
        "DefectRatePercentage",
        "ReceiptRate",
        "AcceptanceRate",
        "TotalItemCost",
        "Cluster"
    ]
]

table_card(
    "Supplier Details",
    "Detailed supplier-level performance and assigned cluster"
)

st.dataframe(
    details.round(2),
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)