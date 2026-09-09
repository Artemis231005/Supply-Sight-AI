import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import plotly.express as px
from utils import load_mart


st.set_page_config(
    page_title="Delivery Delay Prediction",
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
    }
}


def clean_fig(fig):
    fig.update_layout(**PLOTLY_LAYOUT)

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#e7ebf1",
        tickfont={
            "size": 11,
            "color": "#718096"
        }
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#edf1f5",
        zeroline=False,
        linecolor="#e7ebf1",
        tickfont={
            "size": 11,
            "color": "#718096"
        }
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
    "Delivery Delay Prediction",
    "Predict shipment delay risk from distance, transit, freight, and weather conditions.",
)


logistics = load_mart("Logistics_Mart").copy()


st.header("Shipment Overview")

total_shipments = len(logistics)
delayed_shipments = int((logistics["DelayDays"] > 0).sum())
average_delay = logistics["DelayDays"].mean()
on_time_rate = (logistics["DelayDays"] <= 0).mean() * 100


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Shipments", f"{total_shipments:,}")

with c2:
    st.metric("Delayed Shipments", f"{delayed_shipments:,}")

with c3:
    st.metric("Average Delay", f"{average_delay:.2f} days")

with c4:
    st.metric("On-Time Rate", f"{on_time_rate:.1f}%")


for col in [
    "DistanceKM",
    "TransitDays",
    "TemperatureC",
    "HumidityPercent",
    "RainfallMM",
    "WindSpeedKmph",
]:
    logistics[col] = pd.to_numeric(logistics[col], errors="coerce")


model_features = [
    "DistanceKM",
    "TransitDays",
    "TemperatureC",
    "HumidityPercent",
    "RainfallMM",
    "WindSpeedKmph",
]


model_data = logistics[model_features + ["DelayDays"]].dropna().copy()
model_data["Delayed"] = (model_data["DelayDays"] > 0).astype(int)


model = None
accuracy = np.nan
feature_importance = None


if len(model_data) >= 20 and model_data["Delayed"].nunique() == 2:
    X = model_data[model_features]
    y = model_data["Delayed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    feature_importance = (
        pd.DataFrame(
            {
                "Feature": model_features,
                "Importance": model.feature_importances_,
            }
        )
        .sort_values("Importance", ascending=True)
    )


st.header("Predict a Shipment")


st.markdown(
    """
    <div class="chart-card">
        <div class="chart-title">Shipment Prediction Inputs</div>
        <div class="chart-subtitle">
            Enter the planned shipment conditions to estimate whether the shipment is likely to be delayed using Random Forest Model
        </div>
    """,
    unsafe_allow_html=True,
)


input_col1, input_col2 = st.columns(2)


with input_col1:
    input_distance = st.number_input(
        "Distance (KM)",
        min_value=0.0,
        value=float(logistics["DistanceKM"].median()),
        step=10.0,
    )

    input_transit = st.number_input(
        "Transit Days",
        min_value=0.0,
        value=float(logistics["TransitDays"].median()),
        step=1.0,
    )

    input_temperature = st.number_input(
        "Temperature (°C)",
        value=float(logistics["TemperatureC"].median()),
        step=1.0,
    )


with input_col2:
    input_humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(logistics["HumidityPercent"].median()),
        step=1.0,
    )

    input_rainfall = st.number_input(
        "Rainfall (MM)",
        min_value=0.0,
        value=float(logistics["RainfallMM"].median()),
        step=1.0,
    )

    input_wind = st.number_input(
        "Wind Speed (KM/H)",
        min_value=0.0,
        value=float(logistics["WindSpeedKmph"].median()),
        step=1.0,
    )


st.markdown("</div>", unsafe_allow_html=True)


if model is not None:
    if st.button("Predict Delay"):
        input_data = pd.DataFrame(
            [[
                input_distance,
                input_transit,
                input_temperature,
                input_humidity,
                input_rainfall,
                input_wind,
            ]],
            columns=model_features,
        )

        prediction = int(model.predict(input_data)[0])
        probabilities = model.predict_proba(input_data)[0]
        delay_probability = float(probabilities[1] * 100)

        if prediction == 1:
            st.error(
                f"Predicted outcome: DELAYED — estimated delay risk is {delay_probability:.1f}%."
            )
        else:
            st.success(
                f"Predicted outcome: ON TIME — estimated delay risk is {delay_probability:.1f}%."
            )
else:
    st.info("Prediction is unavailable.")


st.metric(
    "Model Accuracy",
    f"{accuracy * 100:.1f}%" if not np.isnan(accuracy) else "N/A"
)

st.markdown("</div>", unsafe_allow_html=True)


st.header("Delay Drivers")


if feature_importance is not None:
    fig = px.bar(
        feature_importance,
        x="Importance",
        y="Feature",
        orientation="h",
    )

    chart_card(
        "Delay Driver Importance",
        "Relative contribution of shipment and weather variables in the Random Forest model",
        clean_fig(fig),
    )
else:
    st.warning(
        "There is not enough class variation or data to train the delay model."
    )


st.header("Delay Analysis")


delay_distribution = (
    logistics.assign(
        DelayStatus=np.where(
            logistics["DelayDays"] > 0,
            "Delayed",
            "On Time",
        )
    )["DelayStatus"]
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Shipments")
)


fig = px.bar(
    delay_distribution,
    x="Status",
    y="Shipments",
)


chart_card(
    "Delay Distribution",
    "Comparison of shipments delivered on time versus shipments with a delay",
    clean_fig(fig),
)


carrier = (
    logistics.assign(OnTime=logistics["DelayDays"] <= 0)
    .groupby("CarrierName")
    .agg(
        Shipments=("CarrierName", "size"),
        AverageDelay=("DelayDays", "mean"),
        OnTimeRate=("OnTime", "mean"),
    )
    .reset_index()
)


carrier["OnTimeRate"] *= 100
carrier = carrier.sort_values("OnTimeRate", ascending=False)


table_card(
    "Carrier Performance",
    "Shipment volume, average delay, and on-time performance by carrier",
)


st.dataframe(
    carrier.round(
        {
            "AverageDelay": 2,
            "OnTimeRate": 1
        }
    ).set_index("CarrierName"),
    use_container_width=True,
)


st.markdown("</div>", unsafe_allow_html=True)