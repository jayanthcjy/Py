CREATE OR REPLACE TABLE SALES_DATA (
    Sale_ID INT AUTOINCREMENT,
    Sale_Date DATE,
    Region STRING,
    Product STRING,
    Quantity INT,
    Unit_Price DECIMAL(10, 2),
    Customer_Info VARIANT -- Added to store JSON data
);




INSERT INTO SALES_DATA (Sale_Date, Region, Product, Quantity, Unit_Price, Customer_Info)
SELECT 
    '2024-01-01', 'North', 'A', 10, 20.00, PARSE_JSON('{"Name": "John", "Email": "john@example.com"}')
UNION ALL
SELECT
    '2024-01-01', 'South', 'B', 5, 50.00, PARSE_JSON('{"Name": "Sarah", "Email": "sarah@example.com"}')
UNION ALL
SELECT
    '2024-01-02', 'North', 'A', 15, 20.00, PARSE_JSON('{"Name": "Emily", "Email": "emily@example.com"}')
UNION ALL
SELECT
    '2024-01-02', 'East', 'C', 8, 40.00, PARSE_JSON('{"Name": "Mark", "Email": "mark@example.com"}');



SELECT * FROM SALES_DATA;

--Step-by-Step Transformation

--1. Basic Aggregation: Total Sales and Revenue by Region and Product

SELECT 
    Region,
    Product,
    SUM(Quantity) AS Total_Sales,
    SUM(Quantity * Unit_Price) AS Total_Revenue
FROM 
    SALES_DATA
GROUP BY 
    Region, Product
ORDER BY 
    Region, Product;

--2. Window Function: Running Total of Sales by Region

WITH Sales_Aggregated AS (
    SELECT 
        Region,
        Product,
        SUM(Quantity) AS Total_Sales,
        SUM(Quantity * Unit_Price) AS Total_Revenue
    FROM 
        SALES_DATA
    GROUP BY 
        Region, Product
)

SELECT
    Region,
    Product,
    Total_Sales,
    Total_Revenue,
    SUM(Total_Sales) OVER (PARTITION BY Region ORDER BY Product) AS Running_Total_Sales
FROM
    Sales_Aggregated
ORDER BY
    Region, Product;

--3. Pivoting Data: Creating a Product Sales Matrix

SELECT 
    Region,
    SUM(CASE WHEN Product = 'A' THEN Quantity ELSE 0 END) AS Product_A_Sales,
    SUM(CASE WHEN Product = 'B' THEN Quantity ELSE 0 END) AS Product_B_Sales,
    SUM(CASE WHEN Product = 'C' THEN Quantity ELSE 0 END) AS Product_C_Sales
FROM 
    SALES_DATA
GROUP BY 
    Region
ORDER BY 
    Region;

--4. JSON Transformation: Extracting Customer Information

SELECT 
    Sale_ID,
    Sale_Date,
    Region,
    Product,
    Quantity,
    Unit_Price,
    Customer_Info:Name::STRING AS Customer_Name,
    Customer_Info:Email::STRING AS Customer_Email
FROM 
    SALES_DATA
WHERE 
    Region = 'North';

--5. Time-Series Data Transformation: Rolling Average Sales

SELECT 
    Sale_Date,
    Region,
    Product,
    Quantity,
    AVG(Quantity) OVER (PARTITION BY Region ORDER BY Sale_Date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS Rolling_Avg_Sales
FROM 
    SALES_DATA
ORDER BY 
    Sale_Date, Region;