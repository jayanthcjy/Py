--1. Create a Share

-- Create a share named NORTH_REGION_SHARE
CREATE SHARE NORTH_REGION_SHARE;

--2.Grant Access to the Table
-- Grant usage on the database and schema to the share
GRANT USAGE ON DATABASE JAY TO SHARE NORTH_REGION_SHARE;
GRANT USAGE ON SCHEMA JAY.PUBLIC TO SHARE NORTH_REGION_SHARE;

-- Grant select access on the SALES_DATA table to the share
GRANT SELECT ON TABLE JAY.PUBLIC.SALES_DATA TO SHARE NORTH_REGION_SHARE;

--3.Restrict Access to North Region Data (Optional)
-- Create a secure view for North region data only
CREATE SECURE VIEW JAY.PUBLIC.NORTH_REGION_SALES AS
SELECT *
FROM JAY.PUBLIC.SALES_DATA
WHERE Region = 'North';

-- Grant select access on the secure view to the share
GRANT SELECT ON VIEW JAY.PUBLIC.NORTH_REGION_SALES TO SHARE NORTH_REGION_SHARE;

--4. Accessing the Shared Data (Consumer Perspective)

--Step 1: Create a Database from the Share
-- Create a database from the shared data
CREATE DATABASE SALES_SHARED_DB FROM SHARE techymart_account_name.NORTH_REGION_SHARE;

--Step 2: Query the Shared Data
-- Query the shared North region sales data
SELECT * FROM SALES_SHARED_DB.PUBLIC.NORTH_REGION_SALES;