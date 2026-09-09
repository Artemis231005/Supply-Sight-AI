from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data_generation"

columns = {
    "Sales_Mart": [
        "SalesID", "DateKey", "FullDate", "Day", "Month", "MonthName",
        "Quarter", "Year", "StoreID", "StoreName", "StoreType",
        "StoreLocationType", "LocationID", "City", "State", "ProductID",
        "ProductName", "Brand", "CategoryID", "Category", "SubCategory",
        "QuantitySold", "ReturnedQuantity", "UnitSellingPrice",
        "DiscountPercentage", "SaleType", "GrossSalesAmount",
        "NetSalesAmount"
    ],

    "Procurement_Mart": [
        "PurchaseOrderItemID", "PurchaseOrderID", "SupplierID",
        "SupplierName", "SupplierSize", "SupplierTier", "SupplierRating",
        "WarehouseID", "WarehouseName", "ProductID", "ProductName", "Brand",
        "CategoryID", "Category", "SubCategory", "OrderDateKey", "OrderDate",
        "ExpectedDeliveryDateKey", "ExpectedDeliveryDate", "LeadTimeDays",
        "MinimumOrderQty", "DefectRatePercentage", "QuantityOrdered",
        "ReceivedQuantity", "AcceptedQuantity", "QuotedUnitCost",
        "TotalItemCost", "InspectionStatus", "LineAmountBeforeTax",
        "TaxRate", "TaxAmount", "LineAmountAfterTax", "ReceiptRate",
        "AcceptanceRate"
    ],

    "Inventory_Mart": [
        "InventoryID", "WarehouseID", "WarehouseName", "WarehouseType",
        "LocationID", "City", "State", "ProductID", "ProductName", "Brand",
        "CategoryID", "Category", "SubCategory", "CurrentStock",
        "ReservedStock", "ReorderLevel", "AvailableStock",
        "LastRestockedDateKey", "LastRestockedDate", "LastIssuedDateKey",
        "LastIssuedDate", "InventoryCondition"
    ],

    "Logistics_Mart": [
        "ShipmentID", "PurchaseOrderID", "SupplierID", "SupplierName",
        "SupplierTier", "WarehouseID", "WarehouseName", "LocationID",
        "City", "State", "CarrierID", "CarrierName", "TransportMode",
        "ShipmentDateKey", "ShipmentDate", "ExpectedDeliveryDateKey",
        "ExpectedDeliveryDate", "ActualDeliveryDateKey", "ActualDeliveryDate",
        "TrackingNumber", "DistanceKM", "TransitDays", "DelayDays",
        "ShipmentStatus", "FreightCost", "OnTimeFlag", "FreightCostPerKM",
        "TemperatureC", "HumidityPercent", "RainfallMM", "WindSpeedKmph",
        "WeatherCondition", "WeatherSeverity"
    ]
}


def load_mart(name):
    file_path = DATA_DIR / f"{name}.csv"

    return pd.read_csv(
        file_path,
        header=None,
        names=columns[name]
    )