DROP DATABASE IF EXISTS SupplySightAI_DW;

CREATE DATABASE SupplySightAI_DW;
USE SupplySightAI_DW;

# Dimension Tables
CREATE TABLE DimLocation (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    City VARCHAR(30),
    State VARCHAR(30),
    UNIQUE (City, State)
);

CREATE TABLE DimCategory (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Category VARCHAR(30),
    SubCategory VARCHAR(50),
    UNIQUE (Category, SubCategory)
);

CREATE TABLE DimProduct (
    ProductID VARCHAR(30) PRIMARY KEY,
    ProductName VARCHAR(100),
    Brand VARCHAR(50),
    CategoryID INT,
    UnitCost DECIMAL(10,2),
    SellingPrice DECIMAL(10,2),
    ShelfLifeDays INT,

    FOREIGN KEY (CategoryID) REFERENCES DimCategory(CategoryID)
);

CREATE TABLE DimStore (
    StoreID VARCHAR(30) PRIMARY KEY,
    StoreName VARCHAR(100),
    StoreType VARCHAR(50),
    LocationID INT,
    StoreLocationType VARCHAR(30),
    Manager VARCHAR(100),
    OpeningYear YEAR,
    FloorAreaSqFt INT,
    ActiveStatus VARCHAR(30),

    FOREIGN KEY (LocationID) REFERENCES DimLocation(LocationID)
);

CREATE TABLE DimWarehouse (
    WarehouseID VARCHAR(30) PRIMARY KEY,
    WarehouseName VARCHAR(100),
    WarehouseType VARCHAR(50),
    LocationID INT,
    Manager VARCHAR(100),
    Capacity INT,
    OperatingHours VARCHAR(30),
    AutomationLevel VARCHAR(30),
    ActiveStatus VARCHAR(30),

    FOREIGN KEY (LocationID) REFERENCES DimLocation(LocationID)
);

CREATE TABLE DimSupplier (
    SupplierID VARCHAR(30) PRIMARY KEY,
    SupplierName VARCHAR(100),
    Phone VARCHAR(30),
    Email VARCHAR(100),
    LocationID INT,
    SupplierSize VARCHAR(30),
    SupplierTier VARCHAR(30),
    Rating DECIMAL(2,1),
    ActiveStatus VARCHAR(30),

    FOREIGN KEY (LocationID) REFERENCES DimLocation(LocationID)
);

CREATE TABLE DimSupplierProduct (
    SupplierID VARCHAR(30),
    ProductID VARCHAR(30),
    LeadTimeDays INT,
    MinimumOrderQty INT,
    QuotedUnitCost DECIMAL(10,2),
    DefectRatePercentage DECIMAL(10,2),

    PRIMARY KEY (SupplierID, ProductID),
    FOREIGN KEY (SupplierID) REFERENCES DimSupplier(SupplierID),
	FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID)
);

CREATE TABLE DimPurchaseOrder (
    PurchaseOrderID VARCHAR(30) PRIMARY KEY,
    SupplierID VARCHAR(30),
    WarehouseID VARCHAR(30),
    OrderDate DATE,
    ExpectedDeliveryDate DATE,
    OrderStatus VARCHAR(30),
    PaymentStatus VARCHAR(30),

    FOREIGN KEY (SupplierID) REFERENCES DimSupplier(SupplierID),
	FOREIGN KEY (WarehouseID) REFERENCES DimWarehouse(WarehouseID)
);

CREATE TABLE DimCarrier (
    CarrierID INT AUTO_INCREMENT PRIMARY KEY,
    CarrierName VARCHAR(50),
    TransportMode VARCHAR(30),
    UNIQUE (CarrierName, TransportMode)
);

CREATE TABLE DimWeather (
    WeatherID VARCHAR(30) PRIMARY KEY,
    LocationID INT,
    RecordedDate DATE,
    TemperatureC INT,
    HumidityPercent DECIMAL(10,2),
    RainfallMM INT,
    WindSpeedKmph INT,
    WeatherCondition VARCHAR(30),
    WeatherSeverity VARCHAR(30),

    FOREIGN KEY (LocationID) REFERENCES DimLocation(LocationID)
);

CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    FullDate DATE UNIQUE,
    Day INT,
    Month INT,
    MonthName VARCHAR(15),
    Quarter INT,
    Year INT,
    Week INT,
    DayOfWeek VARCHAR(15),
    IsWeekend BOOLEAN
);

# Fact Tables
CREATE TABLE FactSales (
    SalesID VARCHAR(30) PRIMARY KEY,
    SalesDateKey INT,
    StoreID VARCHAR(30),
    ProductID VARCHAR(30),
    QuantitySold INT,
    UnitSellingPrice DECIMAL(10,2),
    DiscountPercentage DECIMAL(5,2),
    ReturnedQuantity INT,
    SaleType VARCHAR(30),

    FOREIGN KEY (StoreID) REFERENCES DimStore(StoreID),
    FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
    FOREIGN KEY (SalesDateKey) REFERENCES DimDate(DateKey)
);

CREATE TABLE FactPurchase (
    PurchaseOrderItemID VARCHAR(30) PRIMARY KEY,
    PurchaseOrderID VARCHAR(30),
    ProductID VARCHAR(30),
    OrderDateKey INT,
	ExpectedDeliveryDateKey INT,
    QuantityOrdered INT,
    ReceivedQuantity INT,
    AcceptedQuantity INT,
    QuotedUnitCost DECIMAL(10,2),
    TotalItemCost DECIMAL(10,2),
    InspectionStatus VARCHAR(30),
    LineAmountBeforeTax DECIMAL(10,2),
    TaxRate DECIMAL(10,2),
    TaxAmount DECIMAL(10,2),
    LineAmountAfterTax DECIMAL(10,2),

    FOREIGN KEY (PurchaseOrderID) REFERENCES DimPurchaseOrder(PurchaseOrderID), 
    FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
    FOREIGN KEY (OrderDateKey) REFERENCES DimDate(DateKey),
	FOREIGN KEY (ExpectedDeliveryDateKey) REFERENCES DimDate(DateKey)
);

CREATE TABLE FactShipment (
    ShipmentID VARCHAR(30) PRIMARY KEY,
    PurchaseOrderID VARCHAR(30),
    SupplierID VARCHAR(30),
    WarehouseID VARCHAR(30),
    CarrierID INT,
    ShipmentDateKey INT,
	ExpectedDeliveryDateKey INT,
	ActualDeliveryDateKey INT,
    TrackingNumber VARCHAR(30),
    DistanceKM INT,
    TransitDays INT,
    DelayDays INT,
    ShipmentStatus VARCHAR(30),
    FreightCost DECIMAL(10,2),

    FOREIGN KEY (PurchaseOrderID) REFERENCES DimPurchaseOrder(PurchaseOrderID), 
    FOREIGN KEY (SupplierID) REFERENCES DimSupplier(SupplierID), 
    FOREIGN KEY (WarehouseID) REFERENCES DimWarehouse(WarehouseID),
    FOREIGN KEY (CarrierID) REFERENCES DimCarrier(CarrierID),
    FOREIGN KEY (ShipmentDateKey) REFERENCES DimDate(DateKey),
	FOREIGN KEY (ExpectedDeliveryDateKey) REFERENCES DimDate(DateKey),
	FOREIGN KEY (ActualDeliveryDateKey) REFERENCES DimDate(DateKey)
);

CREATE TABLE FactInventory (
    InventoryID VARCHAR(30) PRIMARY KEY,
    WarehouseID VARCHAR(30),
    ProductID VARCHAR(30),
    CurrentStock INT,
    ReservedStock INT,
    ReorderLevel INT,
    LastRestockedDateKey INT,
	LastIssuedDateKey INT,
    InventoryCondition VARCHAR(30),

    FOREIGN KEY (WarehouseID) REFERENCES DimWarehouse(WarehouseID),
    FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
    FOREIGN KEY (LastRestockedDateKey) REFERENCES DimDate(DateKey),
	FOREIGN KEY (LastIssuedDateKey) REFERENCES DimDate(DateKey)
);


SHOW TABLES;