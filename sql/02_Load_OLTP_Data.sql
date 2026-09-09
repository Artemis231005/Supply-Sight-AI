LOAD DATA LOCAL INFILE 'data_generation/Products Data.csv'
INTO TABLE Products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    ProductSysID,
    ProductID,
    ProductName,
    Brand,
    Category,
    SubCategory,
    UnitCost,
    SellingPrice,
    @ShelfLifeDays
)
SET ShelfLifeDays =
    CASE
        WHEN TRIM(@ShelfLifeDays) = '' THEN NULL
        ELSE ROUND(@ShelfLifeDays)
    END;


SELECT
    COUNT(*) AS TotalRows,
    COUNT(ShelfLifeDays) AS NonNullShelfLife,
    SUM(ShelfLifeDays IS NULL) AS MissingShelfLife,
    SUM(ShelfLifeDays = 0) AS ZeroShelfLife
FROM Products;

LOAD DATA LOCAL INFILE 'data_generation/Warehouse Data.csv'
INTO TABLE Warehouses
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Store Data.csv'
INTO TABLE Stores
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Supplier Data.csv'
INTO TABLE Suppliers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Supplier Products Data.csv'
INTO TABLE SupplierProducts
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Purchase Order Header Data.csv'
INTO TABLE PurchaseOrderHeader
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Purchase Order Items Data.csv'
INTO TABLE PurchaseOrderItems
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Inventory Data.csv'
INTO TABLE Inventory
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Sales Data.csv'
INTO TABLE Sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Weather Data.csv'
INTO TABLE Weather
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data_generation/Shipment Data.csv'
INTO TABLE Shipments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


