import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os

username = os.getenv("DB_USERNAME")
password = quote_plus(os.getenv("DB_PASSWORD"))

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@localhost:3306/SupplySightAI_DW"
)

sales = pd.read_sql("SELECT * FROM SalesMart", engine)
procurement = pd.read_sql("SELECT * FROM ProcurementMart", engine)
inventory = pd.read_sql("SELECT * FROM InventoryMart", engine)
logistics = pd.read_sql("SELECT * FROM LogisticsMart", engine)


print("Sales Shape:", sales.shape)
print("Procurement Shape:", procurement.shape)
print("Inventory Shape:", inventory.shape)
print("Logistics Shape:", logistics.shape)

print("\nSales Columns:")
print(sales.columns.tolist())

print("\nProcurement Columns:")
print(procurement.columns.tolist())

print("\nInventory Columns:")
print(inventory.columns.tolist())

print("\nLogistics Columns:")
print(logistics.columns.tolist())


# Sales Analysis

## Sales Preprocessing
print("Missing Values:")
print(sales.isnull().sum())

print("\nDuplicate Rows:", sales.duplicated().sum())

sales["FullDate"] = pd.to_datetime(sales["FullDate"], errors="coerce")

sales_numeric_cols = [
       "QuantitySold",
       "ReturnedQuantity",
       "UnitSellingPrice",
       "DiscountPercentage",
       "GrossSalesAmount",
       "NetSalesAmount"
]

for col in sales_numeric_cols:
       sales[col] = pd.to_numeric(sales[col], errors="coerce")

sales["ReturnRate"] = np.where(
       sales["QuantitySold"] > 0, 
       sales["ReturnedQuantity"] / sales["QuantitySold"] * 100, 
       0
)

sales["DiscountAmount"] = (sales["GrossSalesAmount"] - sales["NetSalesAmount"])

## Sales KPIs
total_gross_sales = sales["GrossSalesAmount"].sum()
total_net_sales = sales["NetSalesAmount"].sum()
total_units_sold = sales["QuantitySold"].sum()
total_units_returned = sales["ReturnedQuantity"].sum()

overall_return_rate = (
       total_units_returned / total_units_sold * 100
       if total_units_sold > 0 else 0
)

average_sale = sales["NetSalesAmount"].mean()

print(f"Gross Sales       : ₹{total_gross_sales:,.2f}")
print(f"Net Sales         : ₹{total_net_sales:,.2f}")
print(f"Units Sold        : {total_units_sold:,.0f}")
print(f"Units Returned    : {total_units_returned:,.0f}")
print(f"Return Rate       : {overall_return_rate:.2f}%")
print(f"Average Sale      : ₹{average_sale:,.2f}")


## Daily Sales
daily_sales = (
       sales.groupby("FullDate", as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              GrossSales=("GrossSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("FullDate")
)

sns.lineplot(data=daily_sales, x="FullDate", y="NetSales", marker="o")
plt.title("Daily Net Sales Trend")
plt.xlabel("Date")
plt.ylabel("Net Sales")
plt.xticks(rotation=45)
plt.show()

## Monthly Sales
monthly_sales = (
       sales.groupby(["Month", "MonthName"], as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              GrossSales=("GrossSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("Month")
)


sns.lineplot(data=monthly_sales, x="MonthName", y="NetSales", marker="o")
plt.title("Monthly Net Sales Trend")
plt.xlabel("Month")
plt.ylabel("Net Sales")
plt.xticks(rotation=45)
plt.show()


## Performancy by Store Type
store_type_sales = (
       sales.groupby("StoreType", as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum"),
              Transactions=("SalesID", "nunique")
       )
       .sort_values("NetSales", ascending=False)
)

sns.barplot(data=store_type_sales, x="StoreType", y="NetSales")
plt.title("Net Sales by Store Type")
plt.xlabel("Store Type")
plt.ylabel("Net Sales")
plt.show()


## Store Location Type
location_sales = (
       sales.groupby("StoreLocationType", as_index=False)
       .agg(
              TotalNetSales=("NetSalesAmount", "sum"),
              AverageNetSales=("NetSalesAmount", "mean"),
              Transactions=("SalesID", "nunique")
       )
       .sort_values("TotalNetSales", ascending=False)
)

sns.barplot(data=location_sales, x="StoreLocationType", y="TotalNetSales")
plt.title("Total Net Sales by Store Location Type")
plt.xlabel("Store Location Type")
plt.ylabel("Total Net Sales")
plt.show()

# Sales by State
state_sales = (
       sales.groupby("State", as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("NetSales", ascending=False)
)

sns.barplot(data=state_sales, y="State", x="NetSales")
plt.title("Net Sales by State")
plt.xlabel("Net Sales")
plt.ylabel("State")
plt.show()


## Sales by City
city_sales = (
       sales.groupby("City", as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("NetSales", ascending=False)
)

sns.barplot(data=city_sales, y="City", x="NetSales")
plt.title("Net Sales by City")
plt.xlabel("Net Sales")
plt.ylabel("City")
plt.show()


## Category Performance
category_sales = (
       sales.groupby("Category", as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("NetSales", ascending=False)
)

sns.barplot(data=category_sales, x="Category", y="NetSales")
plt.title("Net Sales by Category")
plt.xlabel("Category")
plt.ylabel("Net Sales")
plt.show()


## Top SubCategories
subcategory_sales = (
       sales.groupby(["Category", "SubCategory"], as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("NetSales", ascending=False)
)

sns.barplot(data=subcategory_sales.head(15), x="NetSales", y="SubCategory", hue="Category")
plt.title("Top 15 Subcategories by Net Sales")
plt.xlabel("Net Sales")
plt.ylabel("Subcategory")
plt.show()


## Brand Popularity and Performance
brand_sales = (
       sales.groupby("Brand", as_index=False)
       .agg(
              NetSales=("NetSalesAmount", "sum"),
              QuantitySold=("QuantitySold", "sum")
       )
       .sort_values("NetSales", ascending=False)
)

sns.barplot(data=brand_sales.head(15), x="NetSales", y="Brand")
plt.title("Top 15 Brands by Net Sales")
plt.xlabel("Net Sales")
plt.ylabel("Brand")
plt.show()


## Return Rate by SubCategory
return_analysis = (
       sales.groupby(["Category", "SubCategory"],as_index=False)
       .agg(
              QuantitySold=("QuantitySold", "sum"),
              ReturnedQuantity=("ReturnedQuantity", "sum")
       )
)

return_analysis["ReturnRate"] = np.where(
    return_analysis["QuantitySold"] > 0,
    return_analysis["ReturnedQuantity"] / return_analysis["QuantitySold"] * 100,
    0
)
return_analysis = return_analysis.sort_values("ReturnRate", ascending=False)

sns.barplot(data=return_analysis.head(15), x="ReturnRate", y="SubCategory", hue="Category")
plt.title("Top 15 Subcategories by Return Rate")
plt.xlabel("Return Rate (%)")
plt.ylabel("Subcategory")
plt.show()


## Discount VS Net Sales
sales_sample = sales.sample(
    min(5000, len(sales)),
    random_state=42
)

sns.scatterplot(data=sales_sample, x="DiscountPercentage", y="NetSalesAmount", alpha=0.5)
plt.title("Discount Percentage vs Net Sales")
plt.xlabel("Discount (%)")
plt.ylabel("Net Sales")
plt.show()

print("\nDiscount vs Net Sales Correlation:")
print(sales[["DiscountPercentage", "NetSalesAmount"]].corr())


# PROCUREMENT ANALYSIS

## Procuremnt Preprocessing
print("Missing Values:")
print(procurement.isnull().sum())

print("\nDuplicate Rows:", procurement.duplicated().sum())

procurement_numeric_cols = [
    "SupplierRating",
    "LeadTimeDays",
    "MinimumOrderQty",
    "DefectRatePercentage",
    "QuantityOrdered",
    "ReceivedQuantity",
    "AcceptedQuantity",
    "QuotedUnitCost",
    "TotalItemCost",
    "TaxRate",
    "TaxAmount",
    "LineAmountAfterTax",
    "ReceiptRate",
    "AcceptanceRate"
]

for col in procurement_numeric_cols:
       if col in procurement.columns:
              procurement[col] = pd.to_numeric(procurement[col], errors="coerce")


## Supplier Aggregated Performance
supplier_analysis = (
       procurement.groupby(
              [
              "SupplierID",
              "SupplierName",
              "SupplierSize",
              "SupplierTier"
              ],
              as_index=False
       )
       .agg(
              AvgRating=("SupplierRating", "mean"),
              AvgDefectRate=("DefectRatePercentage", "mean"),
              AvgAcceptanceRate=("AcceptanceRate", "mean"),
              AvgReceiptRate=("ReceiptRate", "mean"),
              TotalQuantityOrdered=("QuantityOrdered", "sum"),
              TotalQuantityReceived=("ReceivedQuantity", "sum"),
              TotalCost=("TotalItemCost", "sum")
       )
)


## Supplier rating Vs Defect Rate
sns.scatterplot(
    data=supplier_analysis,
    x="AvgRating",
    y="AvgDefectRate",
    hue="SupplierTier",
    size="TotalQuantityOrdered",
    alpha=0.8
)
plt.title("Supplier Rating vs Defect Rate")
plt.xlabel("Average Supplier Rating")
plt.ylabel("Average Defect Rate (%)")
plt.show()


## Supplier Size Vs Defect Rate
sns.boxplot(data=procurement, x="SupplierSize", y="DefectRatePercentage")
plt.title("Defect Rate Distribution by Supplier Size")
plt.xlabel("Supplier Size")
plt.ylabel("Defect Rate (%)")
plt.show()


## Supplier Tier Vs Acceptance Rate
tier_analysis = (
       procurement.groupby(
              "SupplierTier",
              as_index=False
       )
       .agg(
              AvgAcceptanceRate=("AcceptanceRate", "mean"),
              AvgDefectRate=("DefectRatePercentage", "mean"),
              AvgSupplierRating=("SupplierRating", "mean")
       )
)

sns.barplot(data=tier_analysis, x="SupplierTier", y="AvgAcceptanceRate")
plt.title("Average Acceptance Rate by Supplier Tier")
plt.xlabel("Supplier Tier")
plt.ylabel("Acceptance Rate (%)")
plt.show()


## Quantity Procured by Catgeory
category_procurement = (
       procurement.groupby(
              "Category",
              as_index=False
       )
       .agg(
              QuantityOrdered=("QuantityOrdered", "sum"),
              QuantityReceived=("ReceivedQuantity", "sum"),
              QuantityAccepted=("AcceptedQuantity", "sum")
       )
)

sns.barplot(data=category_procurement, x="Category", y="QuantityOrdered")
plt.title("Quantity Ordered by Category")
plt.xlabel("Category")
plt.ylabel("Quantity Ordered")
plt.show()


## Procuremnt Cost by Category
category_cost = (
       procurement.groupby(
              "Category",
              as_index=False
       )
       .agg(
              TotalCost=("TotalItemCost", "sum"),
              AvgUnitCost=("QuotedUnitCost", "mean")
       )
       .sort_values(
              "TotalCost",
              ascending=False
       )
)

sns.barplot(data=category_cost, x="Category", y="TotalCost")
plt.title("Procurement Cost by Category")
plt.xlabel("Category")
plt.ylabel("Total Procurement Cost")
plt.show()


# Inventory Analysis

## Inventory Preprocessing
print("Missing Values:")
print(inventory.isnull().sum())

print("\nDuplicate Rows:", inventory.duplicated().sum())

inventory_numeric_cols = [
       "CurrentStock",
       "ReservedStock",
       "ReorderLevel",
       "AvailableStock"
]

for col in inventory_numeric_cols:
       inventory[col] = pd.to_numeric(inventory[col], errors="coerce")

inventory["StockUtilization"] = np.where(
       inventory["CurrentStock"] > 0,
       inventory["ReservedStock"] / inventory["CurrentStock"] * 100,
       0
)

inventory["StockCoverage"] = np.where(
       inventory["ReorderLevel"] > 0,
       inventory["AvailableStock"] / inventory["ReorderLevel"],
       np.nan
)

inventory['InventoryCondition'] = (
       inventory['InventoryCondition']
       .astype(str)
       .str.replace("\r", "", regex=False)
       .str.replace("\n", "", regex=False)
       .str.strip()
)

## Warehouse Distribution by State
warehouse_state = (
       inventory.groupby("State")["WarehouseID"]
       .nunique()
       .reset_index(name="WarehouseCount")
       .sort_values("WarehouseCount", ascending=False)
)

sns.barplot(data=warehouse_state, y="State", x="WarehouseCount")
plt.title("Number of Warehouses by State")
plt.xlabel("Number of Warehouses")
plt.ylabel("State")
plt.show()


## Warehouse Type Distibution
warehouse_type = (
       inventory.groupby("WarehouseType")["WarehouseID"]
       .nunique()
       .reset_index(name="WarehouseCount")
)

sns.barplot(data=warehouse_type, x="WarehouseType", y="WarehouseCount")
plt.title("Warehouse Distribution by Type")
plt.xlabel("Warehouse Type")
plt.ylabel("Number of Warehouses")
plt.show()


## Inventory by category
inventory_category = (
       inventory.groupby(
              "Category",
              as_index=False
       )
       .agg(
              CurrentStock=("CurrentStock", "sum"),
              ReservedStock=("ReservedStock", "sum"),
              AvailableStock=("AvailableStock", "sum"),
              ReorderLevel=("ReorderLevel", "sum")
       )
)

sns.barplot(data=inventory_category, x="Category", y="AvailableStock")
plt.title("Available Inventory by Category")
plt.xlabel("Category")
plt.ylabel("Available Stock")
plt.show()


# Inventory Condition
sns.countplot(data=inventory, x="InventoryCondition", order=inventory["InventoryCondition"].value_counts().index)
plt.title("Inventory Condition Distribution")
plt.xlabel("Inventory Condition")
plt.ylabel("Number of Inventory Records")
plt.xticks(rotation=30)
plt.show()


## Available Stock Vs Reorder Level
inventory_sample = inventory.sample(
       min(5000, len(inventory)),
       random_state=42
)

sns.scatterplot(
       data=inventory_sample,
       x="ReorderLevel",
       y="AvailableStock",
       hue="Category",
       alpha=0.7
)

max_value = max(
       inventory["ReorderLevel"].max(),
       inventory["AvailableStock"].max()
)

plt.plot(
       [0, max_value],
       [0, max_value],
       linestyle="--"
)

plt.title("Available Stock vs Reorder Level")
plt.xlabel("Reorder Level")
plt.ylabel("Available Stock")
plt.show()


# Logistics Analysis

## Logistics Preprocessing
print("Missing Values:")
print(logistics.isnull().sum())

print("\nDuplicate Rows:", logistics.duplicated().sum())

logistics["ShipmentDate"] = pd.to_datetime(
       logistics["ShipmentDate"],
       errors="coerce"
)

logistics["ExpectedDeliveryDate"] = pd.to_datetime(
       logistics["ExpectedDeliveryDate"],
       errors="coerce"
)

logistics["ActualDeliveryDate"] = pd.to_datetime(
       logistics["ActualDeliveryDate"],
       errors="coerce"
)

logistics_numeric_cols = [
    "DistanceKM",
    "TransitDays",
    "DelayDays",
    "FreightCost",
    "OnTimeFlag",
    "FreightCostPerKM",
    "TemperatureC",
    "HumidityPercent",
    "RainfallMM",
    "WindSpeedKmph"
]

for col in logistics_numeric_cols:
       if col in logistics.columns:
              logistics[col] = pd.to_numeric(logistics[col], errors="coerce")

logistics['WeatherSeverity'] = (
       logistics['WeatherSeverity']
       .astype(str)
       .str.replace("\r", "", regex=False)
       .str.replace("\n", "", regex=False)
       .str.strip()
)

weather_order = [
    "Normal",
    "Moderate",
    "High",
    "Severe"
]

## Shipment Status
sns.countplot(data=logistics, x="ShipmentStatus", order=logistics["ShipmentStatus"].value_counts().index)
plt.title("Shipment Status Distribution")
plt.xlabel("Shipment Status")
plt.ylabel("Number of Shipments")
plt.show()


## Delay Distribution
sns.histplot(data=logistics, x="DelayDays", bins=30, kde=True)
plt.title("Distribution of Shipment Delays")
plt.xlabel("Delay (Days)")
plt.ylabel("Number of Shipments")
plt.show()


## Weather Severity Vs Delay
print("\nWeather Severity Distribution:")
print(logistics["WeatherSeverity"].value_counts().reindex(weather_order))

sns.boxplot(data=logistics, x="WeatherSeverity", y="DelayDays", order=weather_order)
plt.title("Shipment Delays by Weather Severity")
plt.xlabel("Weather Severity")
plt.ylabel("Delay (Days)")
plt.show()


## Weather Severity VS On-Time Delivery
weather_ontime = (
       logistics.groupby("WeatherSeverity", as_index=False)
       .agg(
              OnTimeRate=("OnTimeFlag", "mean"),
              AvgDelay=("DelayDays", "mean")
       )
)

weather_ontime["OnTimeRate"] *= 100

sns.barplot(data=weather_ontime, x="WeatherSeverity", y="OnTimeRate", order=weather_order)
plt.title("On-Time Delivery Rate by Weather Severity")
plt.xlabel("Weather Severity")
plt.ylabel("On-Time Delivery Rate (%)")
plt.show()


## Transport Mode VS Delay
mode_delay = (
       logistics.groupby(
              "TransportMode",
              as_index=False
       )
       .agg(
              AvgDelay=("DelayDays", "mean"),
              OnTimeRate=("OnTimeFlag", "mean")
       )
)

mode_delay["OnTimeRate"] *= 100

sns.barplot( data=mode_delay, x="TransportMode", y="AvgDelay")
plt.title("Average Delivery Delay by Transport Mode")
plt.xlabel("Transport Mode")
plt.ylabel("Average Delay (Days)")
plt.show()


## Freight Cost VS Distance
logistics_sample = logistics.sample(
       min(5000, len(logistics)),
       random_state=42
)

sns.scatterplot(
       data=logistics_sample,
       x="DistanceKM",
       y="FreightCost",
       hue="TransportMode",
       alpha=0.6
)

plt.title("Freight Cost vs Shipment Distance")
plt.xlabel("Distance (KM)")
plt.ylabel("Freight Cost")
plt.show()


## Freight Cost Per Km by Transport Mode
mode_cost = (
       logistics.groupby("TransportMode", as_index=False)
       .agg(
              AvgFreightCostPerKM=("FreightCostPerKM", "mean"),
              AvgDistance=("DistanceKM", "mean"),
              AvgFreightCost=("FreightCost", "mean")
       )
)

sns.barplot(data=mode_cost, x="TransportMode", y="AvgFreightCostPerKM")
plt.title("Average Freight Cost per KM by Transport Mode")
plt.xlabel("Transport Mode")
plt.ylabel("Freight Cost per KM")
plt.show()


# Supplier and Loggistics Analysis
supplier_rating = (
       procurement.groupby("SupplierID", as_index=False)
       .agg(
              SupplierRating=("SupplierRating", "mean"),
              DefectRate=("DefectRatePercentage", "mean"),
              AcceptanceRate=("AcceptanceRate", "mean")
       )
)

supplier_delay = (
       logistics.groupby(
              "SupplierID",
              as_index=False
       )
       .agg(
              AvgDelay=("DelayDays", "mean"),
              OnTimeRate=("OnTimeFlag", "mean")
       )
)

supplier_performance = supplier_rating.merge(
       supplier_delay,
       on="SupplierID",
       how="inner"
)

supplier_performance["OnTimeRate"] *= 100


## Suppliier Rating VS Delivery Delay
sns.scatterplot(
       data=supplier_performance,
       x="SupplierRating",
       y="AvgDelay",
       size="AcceptanceRate",
       hue="DefectRate",
       alpha=0.8
)
plt.title("Supplier Rating vs Average Delivery Delay")
plt.xlabel("Supplier Rating")
plt.ylabel("Average Delay (Days)")
plt.show()


