DROP DATABASE IF EXISTS SupplySightAI;

CREATE DATABASE IF NOT EXISTS SupplySightAI;
USE SupplySightAI;

CREATE TABLE IF NOT EXISTS Products (
ProductSysID VARCHAR(30),
ProductID VARCHAR(30) PRIMARY KEY,
ProductName VARCHAR(100),
Brand VARCHAR(50),
Category VARCHAR(30),
SubCategory VARCHAR(50),
UnitCost DECIMAL(10, 2) NOT NULL CHECK (UnitCost >= 0),
SellingPrice DECIMAL(10, 2) NOT NULL CHECK (SellingPrice >= 0),
ShelfLifeDays INT
);

CREATE TABLE IF NOT EXISTS Stores (
StoreSysID VARCHAR(30),
StoreID VARCHAR(30) PRIMARY KEY,
StoreName VARCHAR(100),
StoreType VARCHAR(50),
City VARCHAR(30),
State VARCHAR(30),
StoreLocationType VARCHAR(30),
Manager VARCHAR(100),
OpeningYear YEAR,
FloorAreaSqFt INT,
ActiveStatus VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Warehouses (
WarehouseSysID VARCHAR(30),
WarehouseID VARCHAR(30) PRIMARY KEY,
WarehouseName VARCHAR(100),
WarehouseType VARCHAR(50),
City VARCHAR(30),
State VARCHAR(30),
Manager VARCHAR(100),
Capacity INT CHECK(Capacity >= 0),
OperatingHours VARCHAR(30),
AutomationLevel VARCHAR(30),
ActiveStatus VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Suppliers (
SupplierSysID VARCHAR(30),
SupplierID VARCHAR(30) PRIMARY KEY,
SupplierName VARCHAR(100),
Phone VARCHAR(30) UNIQUE,
Email VARCHAR(100) UNIQUE,
City VARCHAR(30),
State VARCHAR(30),
SupplierSize VARCHAR(30),
SupplierTier VARCHAR(30),
Rating DECIMAL(2, 1) CHECK(Rating BETWEEN 0 AND 5),
ActiveStatus VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS SupplierProducts (
SupplierProductSysID VARCHAR(30),
SupplierID VARCHAR(30),
ProductID VARCHAR(30),
LeadTimeDays INT,
MinimumOrderQty INT,
QuotedUnitCost DECIMAL(10, 2),
DefectRatePercentage DECIMAL(10, 2),

PRIMARY KEY (SupplierID, ProductID),
FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE IF NOT EXISTS PurchaseOrderHeader (
PurchaseOrderSysID VARCHAR(30),
PurchaseOrderID VARCHAR(30) PRIMARY KEY,
SupplierID VARCHAR(30),
WarehouseID VARCHAR(30),
OrderDate DATE,
ExpectedDeliveryDate DATE,
OrderStatus VARCHAR(30),
PaymentStatus VARCHAR(30),

FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
);

CREATE TABLE IF NOT EXISTS PurchaseOrderItems (
PurchaseOrderItemSysID VARCHAR(100),
PurchaseOrderItemID VARCHAR(30) PRIMARY KEY,
PurchaseOrderID VARCHAR(30),
ProductID VARCHAR(30),
QuantityOrdered INT,
ReceivedQuantity INT,
AcceptedQuantity INT,
QuotedUnitCost DECIMAL(10, 2),
TotalItemCost DECIMAL(10, 2),
InspectionStatus VARCHAR(30),
LineAmountBeforeTax DECIMAL(10, 2),
TaxRate DECIMAL(10, 2),
TaxAmount DECIMAL(10, 2),
LineAmountAfterTax DECIMAL(10, 2),

FOREIGN KEY (PurchaseOrderID) REFERENCES PurchaseOrderHeader(PurchaseOrderID),
FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE IF NOT EXISTS Inventory (
InventorySysID VARCHAR(30),
InventoryID VARCHAR(30) PRIMARY KEY,
WarehouseID VARCHAR(30),
ProductID VARCHAR(30),
CurrentStock INT DEFAULT 0,
ReservedStock INT DEFAULT 0,
ReorderLevel INT DEFAULT 0,
LastRestockedDate DATE,
LastIssuedDate DATE,
InventoryCondition VARCHAR(30),

FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID),
FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE IF NOT EXISTS Weather (
WeatherSysID VARCHAR(30),
WeatherID VARCHAR(30) PRIMARY KEY,
City VARCHAR(30),
State VARCHAR(30),
RecordedDate DATE,
TemperatureC INT,
HumidityPercent DECIMAL(10, 2) CHECK(HumidityPercent BETWEEN 0 AND 100),
RainfallMM INT CHECK(RainfallMM >= 0),
WindSpeedKmph INT CHECK(WindSpeedKmph >= 0),
WeatherCondition VARCHAR(30),
WeatherSeverity VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Shipments (
ShipmentSysID VARCHAR(30),
ShipmentID VARCHAR(30) PRIMARY KEY,
PurchaseOrderID VARCHAR(30),
SupplierID VARCHAR(30),
WarehouseID VARCHAR(30),
ShipmentDate DATE,
ExpectedDeliveryDate DATE,
ActualDeliveryDate DATE,
Carrier VARCHAR(50),
TransportMode VARCHAR(30),
TrackingNumber VARCHAR(30),
DistanceKM INT,
TransitDays INT,
DelayDays INT,
ShipmentStatus VARCHAR(30),
FreightCost DECIMAL(10, 2),

FOREIGN KEY (PurchaseOrderID) REFERENCES PurchaseOrderHeader(PurchaseOrderID),
FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
);

CREATE TABLE IF NOT EXISTS Sales (
SalesSysID VARCHAR(30),
SalesID VARCHAR(30) PRIMARY KEY,
SalesDate DATE,
StoreID VARCHAR(30),
ProductID VARCHAR(30),
QuantitySold INT DEFAULT 0 CHECK(QuantitySold >= 0),
UnitSellingPrice DECIMAL(10, 2),
DiscountPercentage DECIMAL(5, 2) CHECK(DiscountPercentage BETWEEN 0 AND 100),
ReturnedQuantity INT DEFAULT 0 CHECK(ReturnedQuantity >= 0),
SaleType VARCHAR(30),

FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);



