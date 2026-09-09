USE SupplySightAI_DW;

# Load data
INSERT INTO DimLocation (City, State)
SELECT DISTINCT City, State
FROM SupplySightAI.Stores
UNION
SELECT DISTINCT City, State
FROM SupplySightAI.Warehouses
UNION
SELECT DISTINCT City, State
FROM SupplySightAI.Suppliers
UNION
SELECT DISTINCT City, State
FROM SupplySightAI.Weather;

INSERT INTO DimCategory (Category, SubCategory)
SELECT DISTINCT Category, SubCategory
FROM SupplySightAI.Products;

INSERT INTO DimProduct
(	ProductID,
    ProductName,
    Brand,
    CategoryID,
    UnitCost,
    SellingPrice,
    ShelfLifeDays
)
SELECT
    p.ProductID,
    p.ProductName,
    p.Brand,
    c.CategoryID,
    p.UnitCost,
    p.SellingPrice,
    p.ShelfLifeDays
FROM SupplySightAI.Products p
JOIN DimCategory c 
	ON p.Category = c.Category
    AND p.SubCategory = c.SubCategory;

INSERT INTO DimStore
(   StoreID,
    StoreName,
    StoreType,
    LocationID,
    StoreLocationType,
    Manager,
    OpeningYear,
    FloorAreaSqFt,
    ActiveStatus
)
SELECT
    s.StoreID,
    s.StoreName,
    s.StoreType,
    l.LocationID,
    s.StoreLocationType,
    s.Manager,
    s.OpeningYear,
    s.FloorAreaSqFt,
    s.ActiveStatus
FROM SupplySightAI.Stores s
JOIN DimLocation l
    ON s.City = l.City
    AND s.State = l.State;

INSERT INTO DimWarehouse
(	WarehouseID,
    WarehouseName,
    WarehouseType,
    LocationID,
    Manager,
    Capacity,
    OperatingHours,
    AutomationLevel,
    ActiveStatus
)
SELECT
    w.WarehouseID,
    w.WarehouseName,
    w.WarehouseType,
    l.LocationID,
    w.Manager,
    w.Capacity,
    w.OperatingHours,
    w.AutomationLevel,
    w.ActiveStatus
FROM SupplySightAI.Warehouses w
JOIN DimLocation l
    ON w.City = l.City
    AND w.State = l.State;

INSERT INTO DimSupplier
(	SupplierID,
    SupplierName,
    Phone,
    Email,
    LocationID,
    SupplierSize,
    SupplierTier,
    Rating,
    ActiveStatus
)
SELECT
    s.SupplierID,
    s.SupplierName,
    s.Phone,
    s.Email,
    l.LocationID,
    s.SupplierSize,
    s.SupplierTier,
    s.Rating,
    s.ActiveStatus
FROM SupplySightAI.Suppliers s
JOIN DimLocation l
    ON s.City = l.City
    AND s.State = l.State;

INSERT INTO DimSupplierProduct
(	SupplierID,
    ProductID,
    LeadTimeDays,
    MinimumOrderQty,
    QuotedUnitCost,
    DefectRatePercentage
)
SELECT
    SupplierID,
    ProductID,
    LeadTimeDays,
    MinimumOrderQty,
    QuotedUnitCost,
    DefectRatePercentage
FROM SupplySightAI.SupplierProducts;

INSERT INTO DimPurchaseOrder
(	PurchaseOrderID,
    SupplierID,
    WarehouseID,
    OrderDate,
    ExpectedDeliveryDate,
    OrderStatus,
    PaymentStatus
)
SELECT
    PurchaseOrderID,
    SupplierID,
    WarehouseID,
    OrderDate,
    ExpectedDeliveryDate,
    OrderStatus,
    PaymentStatus
FROM SupplySightAI.PurchaseOrderHeader;

INSERT INTO DimCarrier
(	CarrierName,
    TransportMode
)
SELECT DISTINCT
    Carrier,
    TransportMode
FROM SupplySightAI.Shipments;

INSERT INTO DimWeather
(	WeatherID,
    LocationID,
    RecordedDate,
    TemperatureC,
    HumidityPercent,
    RainfallMM,
    WindSpeedKmph,
    WeatherCondition,
    WeatherSeverity
)
SELECT
    w.WeatherID,
    l.LocationID,
    w.RecordedDate,
    w.TemperatureC,
    w.HumidityPercent,
    w.RainfallMM,
    w.WindSpeedKmph,
    w.WeatherCondition,
    w.WeatherSeverity
FROM SupplySightAI.Weather w
JOIN DimLocation l
    ON w.City = l.City
    AND w.State = l.State;

INSERT INTO DimDate
(	DateKey,
    FullDate,
    Day,
    Month,
    MonthName,
    Quarter,
    Year,
    Week,
    DayOfWeek,
    IsWeekend
)
SELECT DISTINCT
    DATE_FORMAT(d.FullDate, '%Y%m%d') + 0 AS DateKey,
    d.FullDate,
    DAY(d.FullDate),
    MONTH(d.FullDate),
    MONTHNAME(d.FullDate),
    QUARTER(d.FullDate),
    YEAR(d.FullDate),
    WEEK(d.FullDate),
    DAYNAME(d.FullDate),
    CASE
        WHEN DAYOFWEEK(d.FullDate) IN (1, 7) THEN TRUE
        ELSE FALSE
    END
FROM
(
    SELECT SalesDate AS FullDate
    FROM SupplySightAI.Sales
    UNION
    SELECT OrderDate
    FROM SupplySightAI.PurchaseOrderHeader
    UNION
    SELECT ExpectedDeliveryDate
    FROM SupplySightAI.PurchaseOrderHeader
    UNION
    SELECT ShipmentDate
    FROM SupplySightAI.Shipments
    UNION
    SELECT ExpectedDeliveryDate
    FROM SupplySightAI.Shipments
    UNION
    SELECT ActualDeliveryDate
    FROM SupplySightAI.Shipments
    UNION
    SELECT LastRestockedDate
    FROM SupplySightAI.Inventory
    UNION
    SELECT LastIssuedDate
    FROM SupplySightAI.Inventory
    UNION
    SELECT RecordedDate
    FROM SupplySightAI.Weather
) d
WHERE d.FullDate IS NOT NULL;

INSERT INTO FactSales
(	SalesID,
    SalesDateKey,
    StoreID,
    ProductID,
    QuantitySold,
    UnitSellingPrice,
    DiscountPercentage,
    ReturnedQuantity,
    SaleType
)
SELECT
    s.SalesID,
    DATE_FORMAT(s.SalesDate, '%Y%m%d') + 0,
    s.StoreID,
    s.ProductID,
    s.QuantitySold,
    s.UnitSellingPrice,
    s.DiscountPercentage,
    s.ReturnedQuantity,
    s.SaleType
FROM SupplySightAI.Sales s;

INSERT INTO FactPurchase
(	PurchaseOrderItemID,
    PurchaseOrderID,
    ProductID,
    OrderDateKey,
    ExpectedDeliveryDateKey,
    QuantityOrdered,
    ReceivedQuantity,
    AcceptedQuantity,
    QuotedUnitCost,
    TotalItemCost,
    InspectionStatus,
    LineAmountBeforeTax,
    TaxRate,
    TaxAmount,
    LineAmountAfterTax
)
SELECT
    i.PurchaseOrderItemID,
    i.PurchaseOrderID,
    i.ProductID,
    DATE_FORMAT(h.OrderDate, '%Y%m%d') + 0,
    DATE_FORMAT(h.ExpectedDeliveryDate, '%Y%m%d') + 0,
    i.QuantityOrdered,
    i.ReceivedQuantity,
    i.AcceptedQuantity,
    i.QuotedUnitCost,
    i.TotalItemCost,
    i.InspectionStatus,
    i.LineAmountBeforeTax,
    i.TaxRate,
    i.TaxAmount,
    i.LineAmountAfterTax
FROM SupplySightAI.PurchaseOrderItems i
JOIN SupplySightAI.PurchaseOrderHeader h
    ON i.PurchaseOrderID = h.PurchaseOrderID;

INSERT INTO FactShipment
(	ShipmentID,
    PurchaseOrderID,
    SupplierID,
    WarehouseID,
    CarrierID,
    ShipmentDateKey,
    ExpectedDeliveryDateKey,
    ActualDeliveryDateKey,
    TrackingNumber,
    DistanceKM,
    TransitDays,
    DelayDays,
    ShipmentStatus,
    FreightCost
)
SELECT
    s.ShipmentID,
    s.PurchaseOrderID,
    s.SupplierID,
    s.WarehouseID,
    c.CarrierID,
    DATE_FORMAT(s.ShipmentDate, '%Y%m%d') + 0,
    DATE_FORMAT(s.ExpectedDeliveryDate, '%Y%m%d') + 0,
    DATE_FORMAT(s.ActualDeliveryDate, '%Y%m%d') + 0,
    s.TrackingNumber,
    s.DistanceKM,
    s.TransitDays,
    s.DelayDays,
    s.ShipmentStatus,
    s.FreightCost
FROM SupplySightAI.Shipments s
JOIN DimCarrier c
    ON s.Carrier = c.CarrierName
    AND s.TransportMode = c.TransportMode;

INSERT INTO FactInventory
(	InventoryID,
    WarehouseID,
    ProductID,
    CurrentStock,
    ReservedStock,
    ReorderLevel,
    LastRestockedDateKey,
    LastIssuedDateKey,
    InventoryCondition
)
SELECT
    i.InventoryID,
    i.WarehouseID,
    i.ProductID,
    i.CurrentStock,
    i.ReservedStock,
    i.ReorderLevel,
    DATE_FORMAT(i.LastRestockedDate, '%Y%m%d') + 0,
    DATE_FORMAT(i.LastIssuedDate, '%Y%m%d') + 0,
    i.InventoryCondition
FROM SupplySightAI.Inventory i;

# Validation
# Validate Row Count
SELECT 'DimLocation' AS TableName, COUNT(*) AS RowCount FROM DimLocation
UNION ALL
SELECT 'DimCategory', COUNT(*) FROM DimCategory
UNION ALL
SELECT 'DimProduct', COUNT(*) FROM DimProduct
UNION ALL
SELECT 'DimStore', COUNT(*) FROM DimStore
UNION ALL
SELECT 'DimWarehouse', COUNT(*) FROM DimWarehouse
UNION ALL
SELECT 'DimSupplier', COUNT(*) FROM DimSupplier
UNION ALL
SELECT 'DimSupplierProduct', COUNT(*) FROM DimSupplierProduct
UNION ALL
SELECT 'DimPurchaseOrder', COUNT(*) FROM DimPurchaseOrder
UNION ALL
SELECT 'DimCarrier', COUNT(*) FROM DimCarrier
UNION ALL
SELECT 'DimWeather', COUNT(*) FROM DimWeather
UNION ALL
SELECT 'DimDate', COUNT(*) FROM DimDate
UNION ALL
SELECT 'FactSales', COUNT(*) FROM FactSales
UNION ALL
SELECT 'FactPurchase', COUNT(*) FROM FactPurchase
UNION ALL
SELECT 'FactShipment', COUNT(*) FROM FactShipment
UNION ALL
SELECT 'FactInventory', COUNT(*) FROM FactInventory;

# Validate Relations
SELECT COUNT(*)
FROM FactSales f
LEFT JOIN DimProduct p ON f.ProductID = p.ProductID
WHERE p.ProductID IS NULL;
SELECT COUNT(*)
FROM FactSales f
LEFT JOIN DimStore s ON f.StoreID = s.StoreID
WHERE s.StoreID IS NULL;
SELECT COUNT(*)
FROM FactPurchase f
LEFT JOIN DimProduct p ON f.ProductID = p.ProductID
WHERE p.ProductID IS NULL;
SELECT COUNT(*)
FROM FactShipment f
LEFT JOIN DimCarrier c ON f.CarrierID = c.CarrierID
WHERE c.CarrierID IS NULL;