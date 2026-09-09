USE SupplySightAI_DW;

# DATA MARTS
DROP TABLE IF EXISTS SalesMart;
CREATE TABLE SalesMart AS
SELECT
    f.SalesID,
    d.DateKey,
    d.FullDate,
    d.Day,
    d.Month,
    d.MonthName,
    d.Quarter,
    d.Year,

    f.StoreID,
    s.StoreName,
    s.StoreType,
    s.StoreLocationType,

    l.LocationID,
    l.City,
    l.State,

    f.ProductID,
    p.ProductName,
    p.Brand,

    c.CategoryID,
    c.Category,
    c.SubCategory,

    f.QuantitySold,
    f.ReturnedQuantity,
    f.UnitSellingPrice,
    f.DiscountPercentage,
    f.SaleType,

    f.QuantitySold * f.UnitSellingPrice AS GrossSalesAmount,
    (f.QuantitySold * f.UnitSellingPrice) * (1 - f.DiscountPercentage / 100) AS NetSalesAmount

FROM FactSales f
JOIN DimDate d
    ON f.SalesDateKey = d.DateKey
JOIN DimStore s
    ON f.StoreID = s.StoreID
JOIN DimLocation l
    ON s.LocationID = l.LocationID
JOIN DimProduct p
    ON f.ProductID = p.ProductID
JOIN DimCategory c
    ON p.CategoryID = c.CategoryID;


DROP TABLE IF EXISTS ProcurementMart;
CREATE TABLE ProcurementMart AS
SELECT
    f.PurchaseOrderItemID,
    f.PurchaseOrderID,

    po.SupplierID,
    sup.SupplierName,
    sup.SupplierSize,
    sup.SupplierTier,
    sup.Rating AS SupplierRating,

    po.WarehouseID,
    w.WarehouseName,

    f.ProductID,
    p.ProductName,
    p.Brand,

    c.CategoryID,
    c.Category,
    c.SubCategory,

    f.OrderDateKey,
    od.FullDate AS OrderDate,

    f.ExpectedDeliveryDateKey,
    ed.FullDate AS ExpectedDeliveryDate,

    sp.LeadTimeDays,
    sp.MinimumOrderQty,
    sp.DefectRatePercentage,

    f.QuantityOrdered,
    f.ReceivedQuantity,
    f.AcceptedQuantity,
    f.QuotedUnitCost,
    f.TotalItemCost,
    f.InspectionStatus,
    f.LineAmountBeforeTax,
    f.TaxRate,
    f.TaxAmount,
    f.LineAmountAfterTax,

    CASE
        WHEN f.QuantityOrdered > 0
        THEN f.ReceivedQuantity / f.QuantityOrdered * 100
        ELSE 0
    END AS ReceiptRate,
    CASE
        WHEN f.ReceivedQuantity > 0
        THEN f.AcceptedQuantity / f.ReceivedQuantity * 100
        ELSE 0
    END AS AcceptanceRate

FROM FactPurchase f
JOIN DimPurchaseOrder po
    ON f.PurchaseOrderID = po.PurchaseOrderID
JOIN DimSupplier sup
    ON po.SupplierID = sup.SupplierID
JOIN DimWarehouse w
    ON po.WarehouseID = w.WarehouseID
JOIN DimProduct p
    ON f.ProductID = p.ProductID
JOIN DimCategory c
    ON p.CategoryID = c.CategoryID
LEFT JOIN DimSupplierProduct sp
    ON f.ProductID = sp.ProductID
    AND po.SupplierID = sp.SupplierID
JOIN DimDate od
    ON f.OrderDateKey = od.DateKey
JOIN DimDate ed
    ON f.ExpectedDeliveryDateKey = ed.DateKey;

DROP TABLE IF EXISTS InventoryMart;
CREATE TABLE InventoryMart AS
SELECT
    f.InventoryID,

    f.WarehouseID,
    w.WarehouseName,
    w.WarehouseType,

    wl.LocationID,
    wl.City,
    wl.State,

    f.ProductID,
    p.ProductName,
    p.Brand,

    c.CategoryID,
    c.Category,
    c.SubCategory,

    f.CurrentStock,
    f.ReservedStock,
    f.ReorderLevel,

    f.CurrentStock - f.ReservedStock AS AvailableStock,
    f.LastRestockedDateKey, rd.FullDate AS LastRestockedDate,
    f.LastIssuedDateKey, idt.FullDate AS LastIssuedDate,
    f.InventoryCondition

FROM FactInventory f
JOIN DimWarehouse w
    ON f.WarehouseID = w.WarehouseID
JOIN DimLocation wl
    ON w.LocationID = wl.LocationID
JOIN DimProduct p
    ON f.ProductID = p.ProductID
JOIN DimCategory c
    ON p.CategoryID = c.CategoryID
LEFT JOIN DimDate rd
    ON f.LastRestockedDateKey = rd.DateKey
LEFT JOIN DimDate idt
    ON f.LastIssuedDateKey = idt.DateKey;

DROP TABLE IF EXISTS LogisticsWeather;

CREATE TABLE LogisticsWeather AS
SELECT
    LocationID,
    RecordedDate,
    AVG(TemperatureC) AS TemperatureC,
    AVG(HumidityPercent) AS HumidityPercent,
    SUM(RainfallMM) AS RainfallMM,
    AVG(WindSpeedKmph) AS WindSpeedKmph,
    MAX(WeatherCondition) AS WeatherCondition,
    MAX(WeatherSeverity) AS WeatherSeverity
FROM DimWeather
GROUP BY
    LocationID,
    RecordedDate;

DROP TABLE IF EXISTS LogisticsMart;
CREATE TABLE LogisticsMart AS
SELECT
    f.ShipmentID,
    f.PurchaseOrderID,

    f.SupplierID,
    sup.SupplierName,
    sup.SupplierTier,

    f.WarehouseID,
    w.WarehouseName,

    wl.LocationID,
    wl.City,
    wl.State,

    f.CarrierID,
    car.CarrierName,
    car.TransportMode,

    f.ShipmentDateKey,
    sd.FullDate AS ShipmentDate,

    f.ExpectedDeliveryDateKey,
    ed.FullDate AS ExpectedDeliveryDate,

    f.ActualDeliveryDateKey,
    ad.FullDate AS ActualDeliveryDate,

    f.TrackingNumber,
    f.DistanceKM,
    f.TransitDays,
    f.DelayDays,
    f.ShipmentStatus,
    f.FreightCost,

    CASE
        WHEN f.DelayDays <= 0 THEN 1
        ELSE 0
    END AS OnTimeFlag,
    CASE
        WHEN f.DistanceKM > 0
        THEN f.FreightCost / f.DistanceKM
        ELSE NULL
    END AS FreightCostPerKM,

    we.TemperatureC,
    we.HumidityPercent,
    we.RainfallMM,
    we.WindSpeedKmph,
    we.WeatherCondition,
    we.WeatherSeverity
    
FROM FactShipment f
JOIN DimSupplier sup
    ON f.SupplierID = sup.SupplierID
JOIN DimWarehouse w
    ON f.WarehouseID = w.WarehouseID
JOIN DimLocation wl
    ON w.LocationID = wl.LocationID
JOIN DimCarrier car
    ON f.CarrierID = car.CarrierID
JOIN DimDate sd
    ON f.ShipmentDateKey = sd.DateKey
JOIN DimDate ed
    ON f.ExpectedDeliveryDateKey = ed.DateKey
LEFT JOIN DimDate ad
    ON f.ActualDeliveryDateKey = ad.DateKey
LEFT JOIN LogisticsWeather we
    ON we.LocationID = wl.LocationID
    AND we.RecordedDate = sd.FullDate;

# Analytical Views

# Sales Views
CREATE OR REPLACE VIEW vw_MonthlySalesPerformance AS
SELECT
    Year,
    Month,
    MonthName,
    Category,
    SubCategory,
    SUM(QuantitySold) AS TotalQuantitySold,
    SUM(ReturnedQuantity) AS TotalReturnedQuantity,
    SUM(GrossSalesAmount) AS GrossSales,
    SUM(NetSalesAmount) AS NetSales
FROM SalesMart
GROUP BY
    Year,
    Month,
    MonthName,
    Category,
    SubCategory;

CREATE OR REPLACE VIEW vw_ProductPopularity AS
SELECT
    ProductID,
    ProductName,
    Brand,
    Category,
    SubCategory,
    SUM(QuantitySold) AS TotalUnitsSold,
    SUM(ReturnedQuantity) AS TotalReturns,
    SUM(NetSalesAmount) AS TotalRevenue,
    COUNT(DISTINCT SalesID) AS NumberOfSales
FROM SalesMart
GROUP BY
    ProductID,
    ProductName,
    Brand,
    Category,
    SubCategory;

CREATE OR REPLACE VIEW vw_StorePerformance AS
SELECT
    StoreID,
    StoreName,
    StoreType,
    City,
    State,
    SUM(QuantitySold) AS TotalUnitsSold,
    SUM(NetSalesAmount) AS TotalRevenue,
    COUNT(DISTINCT SalesID) AS NumberOfSales
FROM SalesMart
GROUP BY
    StoreID,
    StoreName,
    StoreType,
    City,
    State;

CREATE OR REPLACE VIEW vw_CategoryPerformance AS
SELECT
    Category,
    SubCategory,
    SUM(QuantitySold) AS TotalUnitsSold,
    SUM(NetSalesAmount) AS TotalRevenue,
    AVG(DiscountPercentage) AS AverageDiscount
FROM SalesMart
GROUP BY
    Category,
    SubCategory;

# Procurement Views
CREATE OR REPLACE VIEW vw_SupplierPerformance AS
SELECT
    SupplierID,
    SupplierName,
    SupplierTier,
    SupplierRating,

    COUNT(DISTINCT PurchaseOrderID) AS TotalPurchaseOrders,

    SUM(QuantityOrdered) AS QuantityOrdered,
    SUM(ReceivedQuantity) AS QuantityReceived,
    SUM(AcceptedQuantity) AS QuantityAccepted,

    AVG(ReceiptRate) AS AverageReceiptRate,
    AVG(AcceptanceRate) AS AverageAcceptanceRate,

    SUM(TotalItemCost) AS TotalPurchaseCost,
    AVG(DefectRatePercentage) AS AverageDefectRate,
    AVG(LeadTimeDays) AS AverageLeadTime
FROM ProcurementMart
GROUP BY
    SupplierID,
    SupplierName,
    SupplierTier,
    SupplierRating;

CREATE OR REPLACE VIEW vw_PurchaseOrderFulfillment AS
SELECT
    PurchaseOrderID,
    SupplierID,
    SupplierName,
    WarehouseID,
    WarehouseName,

    OrderDate,
    ExpectedDeliveryDate,

    SUM(QuantityOrdered) AS QuantityOrdered,
    SUM(ReceivedQuantity) AS QuantityReceived,
    SUM(AcceptedQuantity) AS QuantityAccepted,

    SUM(LineAmountAfterTax) AS TotalOrderValue,

    AVG(ReceiptRate) AS ReceiptRate,
    AVG(AcceptanceRate) AS AcceptanceRate
FROM ProcurementMart
GROUP BY
    PurchaseOrderID,
    SupplierID,
    SupplierName,
    WarehouseID,
    WarehouseName,
    OrderDate,
    ExpectedDeliveryDate;

CREATE OR REPLACE VIEW vw_ProductProcurementCost AS
SELECT
    ProductID,
    ProductName,
    Category,
    SubCategory,
    AVG(QuotedUnitCost) AS AverageQuotedUnitCost,
    SUM(QuantityOrdered) AS TotalQuantityOrdered,
    SUM(TotalItemCost) AS TotalProcurementCost
FROM ProcurementMart
GROUP BY
    ProductID,
    ProductName,
    Category,
    SubCategory;

# Inventory Views
CREATE OR REPLACE VIEW vw_InventoryHealth AS
SELECT
    ProductID,
    ProductName,
    Category,
    SubCategory,

    SUM(CurrentStock) AS CurrentStock,
    SUM(ReservedStock) AS ReservedStock,
    SUM(AvailableStock) AS AvailableStock,
    SUM(ReorderLevel) AS ReorderLevel,

    CASE
        WHEN SUM(AvailableStock) <= SUM(ReorderLevel)
        THEN 'Reorder Required'
        ELSE 'Sufficient Stock'
    END AS StockStatus
FROM InventoryMart
GROUP BY
    ProductID,
    ProductName,
    Category,
    SubCategory;

CREATE OR REPLACE VIEW vw_WarehouseInventory AS
SELECT
    WarehouseID,
    WarehouseName,
    City,
    State,

    SUM(CurrentStock) AS TotalCurrentStock,
    SUM(ReservedStock) AS TotalReservedStock,
    SUM(AvailableStock) AS TotalAvailableStock,
    SUM(ReorderLevel) AS TotalReorderLevel,

    COUNT(DISTINCT ProductID) AS NumberOfProducts,
    SUM(
        CASE
            WHEN AvailableStock <= ReorderLevel
            THEN 1
            ELSE 0
        END
    ) AS ProductsBelowReorderLevel

FROM InventoryMart
GROUP BY
    WarehouseID,
    WarehouseName,
    City,
    State;

CREATE OR REPLACE VIEW vw_StockRisk AS
SELECT
    ProductID,
    ProductName,
    Category,
    SubCategory,
    WarehouseID,
    WarehouseName,
    CurrentStock,
    ReservedStock,
    AvailableStock,
    ReorderLevel,

    CASE
        WHEN AvailableStock = 0 THEN 'Stock Out'
        WHEN AvailableStock <= ReorderLevel THEN 'High Risk'
        WHEN AvailableStock <= ReorderLevel * 1.5 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS StockRisk
FROM InventoryMart;

# Logistics Views
CREATE OR REPLACE VIEW vw_ShipmentPerformance AS
SELECT
    CarrierName,
    TransportMode,

    COUNT(*) AS TotalShipments,
    SUM(OnTimeFlag) AS OnTimeShipments,

    AVG(DelayDays) AS AverageDelayDays,
    AVG(TransitDays) AS AverageTransitDays,

    SUM(FreightCost) AS TotalFreightCost,
    AVG(FreightCostPerKM) AS AverageFreightCostPerKM
FROM LogisticsMart
GROUP BY
    CarrierName,
    TransportMode;

CREATE OR REPLACE VIEW vw_CarrierPerformance AS
SELECT
    CarrierID,
    CarrierName,
    TransportMode,

    COUNT(*) AS TotalShipments,
    SUM(OnTimeFlag) AS OnTimeShipments,
    ROUND(
        SUM(OnTimeFlag) * 100.0 / COUNT(*),
        2
    ) AS OnTimeDeliveryPercentage,

    AVG(DelayDays) AS AverageDelayDays,
    AVG(TransitDays) AS AverageTransitDays,
    SUM(FreightCost) AS TotalFreightCost
FROM LogisticsMart
GROUP BY
    CarrierID,
    CarrierName,
    TransportMode;

CREATE OR REPLACE VIEW vw_DeliveryDelayAnalysis AS
SELECT
    SupplierID,
    SupplierName,
    WarehouseID,
    WarehouseName,
    CarrierName,
    TransportMode,

    COUNT(*) AS TotalShipments,
    AVG(DistanceKM) AS AverageDistanceKM,
    AVG(TransitDays) AS AverageTransitDays,
    AVG(DelayDays) AS AverageDelayDays,
    SUM(
        CASE
            WHEN DelayDays > 0 THEN 1
            ELSE 0
        END
    ) AS DelayedShipments,
    SUM(FreightCost) AS TotalFreightCost
FROM LogisticsMart
GROUP BY
    SupplierID,
    SupplierName,
    WarehouseID,
    WarehouseName,
    CarrierName,
    TransportMode;

CREATE OR REPLACE VIEW vw_WeatherShipmentImpact AS
SELECT
    WeatherSeverity,
    WeatherCondition,

    COUNT(*) AS TotalShipments,
    AVG(RainfallMM) AS AverageRainfallMM,
    AVG(WindSpeedKmph) AS AverageWindSpeedKmph,

    AVG(TransitDays) AS AverageTransitDays,
    AVG(DelayDays) AS AverageDelayDays,
    SUM(
        CASE
            WHEN DelayDays > 0 THEN 1
            ELSE 0
        END
    ) AS DelayedShipments,
    ROUND(
        AVG(OnTimeFlag) * 100,
        2
    ) AS OnTimeDeliveryPercentage
    
FROM LogisticsMart
WHERE WeatherSeverity IS NOT NULL
GROUP BY
    WeatherSeverity,
    WeatherCondition;

# Validation 
SELECT COUNT(*) AS SalesMartRows
FROM SalesMart;

SELECT COUNT(*) AS ProcurementMartRows
FROM ProcurementMart;

SELECT COUNT(*) AS InventoryMartRows
FROM InventoryMart;

SELECT COUNT(*) AS LogisticsMartRows
FROM LogisticsMart;