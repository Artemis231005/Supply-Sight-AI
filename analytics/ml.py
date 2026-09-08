import os
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from urllib.parse import quote_plus

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    RandomForestClassifier
)
from sklearn.cluster import KMeans

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    silhouette_score
)

username = os.getenv("DB_USERNAME")
password = quote_plus(os.getenv("DB_PASSWORD"))

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@localhost:3306/SupplySightAI_DW"
)

sales = pd.read_sql("SELECT * FROM SalesMart", engine)
procurement = pd.read_sql("SELECT * FROM ProcurementMart", engine)
logistics = pd.read_sql("SELECT * FROM LogisticsMart", engine)

# Sales Forecasting: Predict today's NetSalesAmount using information from previous days.

## Feature Engineering
daily_sales = (
    sales
    .groupby("FullDate", as_index=False)["NetSalesAmount"]
    .sum()
    .sort_values("FullDate")
)

daily_sales["FullDate"] = pd.to_datetime(daily_sales["FullDate"])

# Calendar features
daily_sales["DayOfWeek"] = daily_sales["FullDate"].dt.dayofweek
daily_sales["Month"] = daily_sales["FullDate"].dt.month

# Lag features
daily_sales["Lag_1"] = daily_sales["NetSalesAmount"].shift(1)
daily_sales["Lag_2"] = daily_sales["NetSalesAmount"].shift(2)
daily_sales["Lag_3"] = daily_sales["NetSalesAmount"].shift(3)
daily_sales["Lag_7"] = daily_sales["NetSalesAmount"].shift(7)
daily_sales["Lag_14"] = daily_sales["NetSalesAmount"].shift(14)
daily_sales["Lag_28"] = daily_sales["NetSalesAmount"].shift(28)

# Rolling features
daily_sales["Rolling_7"] = (
    daily_sales["NetSalesAmount"]
    .shift(1)
    .rolling(7)
    .mean()
)

daily_sales["Rolling_14"] = (
    daily_sales["NetSalesAmount"]
    .shift(1)
    .rolling(14)
    .mean()
)

daily_sales["Rolling_28"] = (
    daily_sales["NetSalesAmount"]
    .shift(1)
    .rolling(28)
    .mean()
)

daily_sales = daily_sales.dropna().reset_index(drop=True)

# One-hot encode calendar features
daily_sales = pd.get_dummies(
    daily_sales,
    columns=["DayOfWeek", "Month"],
    dtype=int
)

sales_features = [
    "Lag_1",
    "Lag_2",
    "Lag_3",
    "Lag_7",
    "Lag_14",
    "Lag_28",
    "Rolling_7",
    "Rolling_14",
    "Rolling_28"
]

# Add one-hot encoded calendar features
sales_features += [
    col for col in daily_sales.columns
    if col.startswith("DayOfWeek_") or col.startswith("Month_")
]

## Data Split
X_sales = daily_sales[sales_features]
y_sales = daily_sales["NetSalesAmount"]

split = int(len(daily_sales) * 0.8)

X_train_sales = X_sales.iloc[:split]
X_test_sales = X_sales.iloc[split:]

y_train_sales = y_sales.iloc[:split]
y_test_sales = y_sales.iloc[split:]

## Linear Regression Model
lr_model_sales = LinearRegression()
lr_model_sales.fit(X_train_sales, y_train_sales)
sales_lr_pred = lr_model_sales.predict(X_test_sales)

## Model Evaluation
mae = mean_absolute_error(y_test_sales, sales_lr_pred)
rmse = np.sqrt(mean_squared_error(y_test_sales, sales_lr_pred))
r2 = r2_score(y_test_sales, sales_lr_pred)
mape = mean_absolute_percentage_error(y_test_sales, sales_lr_pred)

print("Linear Regression Results: ")
print("MAE  :", mae)
print("RMSE :", rmse)
print("R²   :", r2)
print("MAPE :", mape * 100, "%")


## Naive Baseline
sales_naive_pred = daily_sales["Lag_1"].iloc[split:]

naive_mape = mean_absolute_percentage_error(
    y_test_sales,
    sales_naive_pred
)

naive_mae = mean_absolute_error(y_test_sales, sales_naive_pred)
naive_rmse = np.sqrt(mean_squared_error(y_test_sales, sales_naive_pred))

## Model Evaluation
print("\nNaive Results: ")
print("Naive MAE :", naive_mae)
print("Naive RMSE:", naive_rmse)
print("Naive MAPE:", naive_mape * 100, "%")


## Random Forest
sales_rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

sales_rf_model.fit(X_train_sales, y_train_sales)
sales_rf_pred = sales_rf_model.predict(X_test_sales)

## Model Evaulation
rf_mae = mean_absolute_error(y_test_sales, sales_rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test_sales, sales_rf_pred))
rf_r2 = r2_score(y_test_sales, sales_rf_pred)
rf_mape = mean_absolute_percentage_error(y_test_sales, sales_rf_pred)

print("\nRandom Forest Results")
print("MAE  :", rf_mae)
print("RMSE :", rf_rmse)
print("R²   :", rf_r2)
print("MAPE :", rf_mape * 100, "%")


## Gradient Boosting
sales_gb_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

sales_gb_model.fit(X_train_sales, y_train_sales)
sales_gb_pred = sales_gb_model.predict(X_test_sales)

## Model Evaluation
gb_mae = mean_absolute_error(y_test_sales, sales_gb_pred)
gb_rmse = np.sqrt(mean_squared_error(y_test_sales, sales_gb_pred))
gb_r2 = r2_score(y_test_sales, sales_gb_pred)
gb_mape = mean_absolute_percentage_error(y_test_sales, sales_gb_pred)

print("\nGradient Boosting Results")
print("MAE  :", gb_mae)
print("RMSE :", gb_rmse)
print("R²   :", gb_r2)
print("MAPE :", gb_mape * 100, "%")


# Delivery Delay Prediction: Predict whether a shipment will be delayed or delivered on time.
## Feature Engineering
target = "OnTimeFlag"

# Features
logistics = pd.get_dummies(
    logistics,
    columns=["SupplierTier", "TransportMode", "WeatherSeverity"],
    dtype=int
)

delivery_features = [
    "DistanceKM",
    "TransitDays",
    "FreightCost",
    "FreightCostPerKM",
    "TemperatureC",
    "HumidityPercent",
    "RainfallMM",
    "WindSpeedKmph"
]

delivery_features += [
    col for col in logistics.columns
    if col.startswith("SupplierTier_")
    or col.startswith("TransportMode_")
    or col.startswith("WeatherSeverity_")
]

weather_cols = [
    "TemperatureC",
    "HumidityPercent",
    "RainfallMM",
    "WindSpeedKmph"
]


X = logistics[delivery_features]
y = logistics["OnTimeFlag"]

## Split Data
X_train_delivery, X_test_delivery, y_train_delivery, y_test_delivery = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train_delivery[weather_cols] = X_train_delivery[weather_cols].fillna(
    X_train_delivery[weather_cols].median()
)

X_test_delivery[weather_cols] = X_test_delivery[weather_cols].fillna(
    X_train_delivery[weather_cols].median()
)

scaler = StandardScaler()
X_train_scaled_delivery = scaler.fit_transform(X_train_delivery)
X_test_scaled_delivery = scaler.transform(X_test_delivery)


## Logistic Regression: Baseline
delivery_logistic_model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)
delivery_logistic_model.fit(X_train_scaled_delivery, y_train_delivery)
delivery_lr_y_pred = delivery_logistic_model.predict(X_test_scaled_delivery)

## Model Evaluation
print("\nLogistic Regression Results")
print("Accuracy :", accuracy_score(y_test_delivery, delivery_lr_y_pred))
print("Precision:", precision_score(y_test_delivery, delivery_lr_y_pred))
print("Recall   :", recall_score(y_test_delivery, delivery_lr_y_pred))
print("F1 Score :", f1_score(y_test_delivery, delivery_lr_y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test_delivery, delivery_lr_y_pred))

print("\nClassification Report:")
print(classification_report(y_test_delivery, delivery_lr_y_pred))


## Random Forest
delivery_rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

delivery_rf_model.fit(X_train_delivery, y_train_delivery)
delivery_rf_y_pred = delivery_rf_model.predict(X_test_delivery)

# Model Evaluation
print("\nRandom Forest Results")
print("Accuracy :", accuracy_score(y_test_delivery, delivery_rf_y_pred))
print("Precision:", precision_score(y_test_delivery, delivery_rf_y_pred))
print("Recall   :", recall_score(y_test_delivery, delivery_rf_y_pred))
print("F1 Score :", f1_score(y_test_delivery, delivery_rf_y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test_delivery, delivery_rf_y_pred))

print("\nClassification Report:")
print(classification_report(y_test_delivery, delivery_rf_y_pred))


# Supplier Clustering

## Feature Engineering
supplier_proc = procurement.groupby("SupplierID").agg(
    SupplierName=("SupplierName", "first"),
    SupplierRating=("SupplierRating", "mean"),
    
    AvgLeadTimeDays=("LeadTimeDays", "mean"),
    AvgDefectRate=("DefectRatePercentage", "mean"),
    AvgReceiptRate=("ReceiptRate", "mean"),
    AvgAcceptanceRate=("AcceptanceRate", "mean"),
    
    TotalQuantityOrdered=("QuantityOrdered", "sum"),
    TotalQuantityReceived=("ReceivedQuantity", "sum"),
    TotalQuantityAccepted=("AcceptedQuantity", "sum"),
    AvgQuotedUnitCost=("QuotedUnitCost", "mean"),
    TotalProcurementCost=("TotalItemCost", "sum"),
    
    NumberOfOrders=("PurchaseOrderID", "nunique"),
    NumberOfProducts=("ProductID", "nunique"),
    NumberOfWarehouses=("WarehouseID", "nunique")
).reset_index()

supplier_logistics = logistics.groupby("SupplierID").agg(
    AvgDistanceKM=("DistanceKM", "mean"),
    AvgTransitDays=("TransitDays", "mean"),
    AvgDelayDays=("DelayDays", "mean"),

    TotalFreightCost=("FreightCost", "sum"),
    AvgFreightCostPerKM=("FreightCostPerKM", "mean"),

    OnTimeDeliveryRate=("OnTimeFlag", "mean"),
    NumberOfShipments=("ShipmentID", "nunique")

).reset_index()

supplier_df = supplier_proc.merge(
    supplier_logistics,
    on="SupplierID",
    how="left"
)

numeric_cols = supplier_df.select_dtypes(include=np.number).columns
supplier_df[numeric_cols] = supplier_df[numeric_cols].fillna(0)

supplier_df["AvgQuantityPerOrder"] = (
    supplier_df["TotalQuantityOrdered"] / supplier_df["NumberOfOrders"]
)

supplier_df["AvgCostPerOrder"] = (
    supplier_df["TotalProcurementCost"] / supplier_df["NumberOfOrders"]
)

supplier_df[["AvgQuantityPerOrder", "AvgCostPerOrder"]] = (
    supplier_df[["AvgQuantityPerOrder", "AvgCostPerOrder"]]
    .replace([np.inf, -np.inf], np.nan)
    .fillna(0)
)

supplier_features = [
    "SupplierRating",
    "AvgLeadTimeDays",
    "AvgDefectRate",
    "AvgDelayDays",
    "AvgQuantityPerOrder",
    "AvgCostPerOrder"
]

X_supplier = supplier_df[supplier_features]

scaler = StandardScaler()
X_scaled_supplier = scaler.fit_transform(X_supplier)

# ## Silhouette Score

# for k in range(2, 9):
#     model = KMeans(
#         n_clusters=k,
#         random_state=42,
#         n_init="auto"
#     )

#     labels = model.fit_predict(X_scaled_supplier)
#     score = silhouette_score(X_scaled_supplier, labels)
#     print(f"K = {k} | Silhouette Score = {score:.4f}")
#     # Highest obatined K is 2

best_k = 2

supplier_kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init="auto"
)

supplier_df["Cluster"] = supplier_kmeans.fit_predict(
    X_scaled_supplier
)

print(supplier_df["Cluster"].value_counts().sort_index())

cluster_profile = supplier_df.groupby("Cluster")[supplier_features].mean()
cluster_profile.round(2)

overall_mean = supplier_df[supplier_features].mean()
cluster_vs_overall = (cluster_profile / overall_mean).round(2)

for col in cluster_vs_overall:
    print(cluster_vs_overall[col])

