
--1. Analyzing Query Performance
EXPLAIN
SELECT 
    Region, 
    Product, 
    SUM(Quantity) AS Total_Quantity, 
    SUM(Quantity * Unit_Price) AS Total_Sales
FROM SALES_DATA
WHERE Sale_Date BETWEEN '2024-01-01' AND '2024-01-02'
GROUP BY Region, Product;

--2. Implementing Clustering Keys
ALTER TABLE SALES_DATA
CLUSTER BY (Sale_Date);

--3. Creating Views
CREATE OR REPLACE VIEW v_sales_summary AS
SELECT 
    Region, 
    Product, 
    SUM(Quantity) AS Total_Quantity, 
    SUM(Quantity * Unit_Price) AS Total_Sales
FROM SALES_DATA
GROUP BY Region, Product;

--4. Using Result Caching
SELECT 
    Region, 
    Product, 
    SUM(Quantity) AS Total_Quantity, 
    SUM(Quantity * Unit_Price) AS Total_Sales
FROM SALES_DATA
WHERE Sale_Date BETWEEN '2024-01-01' AND '2024-01-02'
GROUP BY Region, Product;

5. Data Compression
Check the status of views:
DESC VIEW v_sales_summary;

Monitor clustering depth:
SELECT SYSTEM$CLUSTERING_DEPTH('SALES_DATA');



