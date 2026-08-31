-- ============================================================
-- E-COMMERCE DATA ANALYTICS
-- SQL ANALYSIS
-- ============================================================

USE ecommerce_analytics;


-- ============================================================
-- 1. DATA OVERVIEW
-- ============================================================

-- Total number of records
SELECT
    COUNT(*) AS total_records
FROM ecommerce_sales;


-- Number of unique customers
SELECT
    COUNT(DISTINCT customerid) AS unique_customers
FROM ecommerce_sales;


-- Number of unique products
SELECT
    COUNT(DISTINCT product) AS unique_products
FROM ecommerce_sales;


-- Date range of the dataset
SELECT
    MIN(date) AS start_date,
    MAX(date) AS end_date
FROM ecommerce_sales;


-- ============================================================
-- 2. DATA QUALITY CHECK
-- ============================================================

-- Check NULL values
SELECT
    SUM(orderid IS NULL) AS null_orderid,
    SUM(date IS NULL) AS null_date,
    SUM(customerid IS NULL) AS null_customerid,
    SUM(product IS NULL) AS null_product,
    SUM(quantity IS NULL) AS null_quantity,
    SUM(unitprice IS NULL) AS null_unitprice,
    SUM(paymentmethod IS NULL) AS null_paymentmethod,
    SUM(orderstatus IS NULL) AS null_orderstatus,
    SUM(totalprice IS NULL) AS null_totalprice
FROM ecommerce_sales;


-- Check duplicate order IDs
SELECT
    orderid,
    COUNT(*) AS duplicate_count
FROM ecommerce_sales
GROUP BY orderid
HAVING COUNT(*) > 1;


-- Check invalid quantities
SELECT *
FROM ecommerce_sales
WHERE quantity <= 0;


-- Check invalid prices
SELECT *
FROM ecommerce_sales
WHERE unitprice < 0
   OR totalprice < 0;


-- ============================================================
-- 3. OVERALL SALES PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customerid) AS unique_customers,
    COUNT(DISTINCT product) AS unique_products,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(totalprice), 2) AS total_revenue,
    ROUND(AVG(totalprice), 2) AS average_order_value,
    ROUND(MIN(totalprice), 2) AS minimum_order_value,
    ROUND(MAX(totalprice), 2) AS maximum_order_value
FROM ecommerce_sales;


-- ============================================================
-- 4. PRODUCT PERFORMANCE
-- ============================================================

SELECT
    product,
    COUNT(*) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(totalprice), 2) AS total_revenue,
    ROUND(AVG(totalprice), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY product
ORDER BY total_revenue DESC;


-- Top 5 products by revenue
SELECT
    product,
    ROUND(SUM(totalprice), 2) AS revenue
FROM ecommerce_sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;


-- Top 5 products by quantity sold
SELECT
    product,
    SUM(quantity) AS units_sold
FROM ecommerce_sales
GROUP BY product
ORDER BY units_sold DESC
LIMIT 5;


-- ============================================================
-- 5. CUSTOMER ANALYSIS
-- ============================================================

SELECT
    customerid,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_items,
    ROUND(SUM(totalprice), 2) AS total_spent,
    ROUND(AVG(totalprice), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY customerid
ORDER BY total_spent DESC;


-- Top 10 customers by spending
SELECT
    customerid,
    COUNT(*) AS total_orders,
    ROUND(SUM(totalprice), 2) AS total_spent
FROM ecommerce_sales
GROUP BY customerid
ORDER BY total_spent DESC
LIMIT 10;


-- Customers with multiple orders
SELECT
    customerid,
    COUNT(*) AS order_count
FROM ecommerce_sales
GROUP BY customerid
HAVING COUNT(*) > 1
ORDER BY order_count DESC;


-- ============================================================
-- 6. ORDER STATUS ANALYSIS
-- ============================================================

SELECT
    orderstatus,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ecommerce_sales),
        2
    ) AS order_percentage
FROM ecommerce_sales
GROUP BY orderstatus
ORDER BY order_count DESC;


-- ============================================================
-- 7. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    paymentmethod,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue,
    ROUND(AVG(totalprice), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY paymentmethod
ORDER BY revenue DESC;


-- ============================================================
-- 8. REFERRAL SOURCE ANALYSIS
-- ============================================================

SELECT
    referralsource,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue,
    ROUND(AVG(totalprice), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY referralsource
ORDER BY revenue DESC;


-- ============================================================
-- 9. COUPON ANALYSIS
-- ============================================================

SELECT
    couponcode,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue
FROM ecommerce_sales
GROUP BY couponcode
ORDER BY order_count DESC;


-- ============================================================
-- 10. DAILY SALES ANALYSIS
-- ============================================================

SELECT
    date,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    ROUND(SUM(totalprice), 2) AS daily_revenue
FROM ecommerce_sales
GROUP BY date
ORDER BY date;


-- Top 10 highest-revenue days
SELECT
    date,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS daily_revenue
FROM ecommerce_sales
GROUP BY date
ORDER BY daily_revenue DESC
LIMIT 10;


-- ============================================================
-- 11. MONTHLY SALES ANALYSIS
-- ============================================================

SELECT
    YEAR(date) AS year,
    MONTH(date) AS month,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    ROUND(SUM(totalprice), 2) AS monthly_revenue
FROM ecommerce_sales
GROUP BY YEAR(date), MONTH(date)
ORDER BY year, month;


-- ============================================================
-- 12. YEARLY SALES ANALYSIS
-- ============================================================

SELECT
    YEAR(date) AS year,
    COUNT(*) AS order_count,
    SUM(quantity) AS units_sold,
    ROUND(SUM(totalprice), 2) AS yearly_revenue
FROM ecommerce_sales
GROUP BY YEAR(date)
ORDER BY year;


-- ============================================================
-- 13. DAY-OF-WEEK ANALYSIS
-- ============================================================

SELECT
    DAYNAME(date) AS day_of_week,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue
FROM ecommerce_sales
GROUP BY DAYNAME(date), DAYOFWEEK(date)
ORDER BY DAYOFWEEK(date);


-- ============================================================
-- 14. UNIT PRICE ANALYSIS
-- ============================================================

SELECT
    product,
    ROUND(AVG(unitprice), 2) AS average_unit_price,
    ROUND(MIN(unitprice), 2) AS minimum_unit_price,
    ROUND(MAX(unitprice), 2) AS maximum_unit_price
FROM ecommerce_sales
GROUP BY product
ORDER BY average_unit_price DESC;


-- ============================================================
-- 15. ITEMS IN CART ANALYSIS
-- ============================================================

SELECT
    itemsincart,
    COUNT(*) AS order_count,
    ROUND(AVG(totalprice), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY itemsincart
ORDER BY itemsincart;


-- ============================================================
-- 16. HIGH-VALUE ORDERS
-- ============================================================

SELECT
    orderid,
    date,
    customerid,
    product,
    quantity,
    ROUND(unitprice, 2) AS unit_price,
    ROUND(totalprice, 2) AS total_price,
    orderstatus
FROM ecommerce_sales
ORDER BY totalprice DESC
LIMIT 10;


-- ============================================================
-- 17. PRODUCT + PAYMENT ANALYSIS
-- ============================================================

SELECT
    product,
    paymentmethod,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue
FROM ecommerce_sales
GROUP BY product, paymentmethod
ORDER BY revenue DESC;


-- ============================================================
-- 18. PRODUCT + ORDER STATUS ANALYSIS
-- ============================================================

SELECT
    product,
    orderstatus,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue
FROM ecommerce_sales
GROUP BY product, orderstatus
ORDER BY revenue DESC;


-- ============================================================
-- 19. REFERRAL SOURCE + PRODUCT ANALYSIS
-- ============================================================

SELECT
    referralsource,
    product,
    COUNT(*) AS order_count,
    ROUND(SUM(totalprice), 2) AS revenue
FROM ecommerce_sales
GROUP BY referralsource, product
ORDER BY revenue DESC;


-- ============================================================
-- 20. CANCELLED ORDERS
-- ============================================================

SELECT
    COUNT(*) AS cancelled_orders,
    ROUND(SUM(totalprice), 2) AS cancelled_revenue
FROM ecommerce_sales
WHERE LOWER(orderstatus) = 'cancelled';


-- ============================================================
-- 21. SUCCESSFUL ORDERS
-- ============================================================

SELECT
    COUNT(*) AS successful_orders,
    ROUND(SUM(totalprice), 2) AS successful_revenue
FROM ecommerce_sales
WHERE LOWER(orderstatus) IN ('completed', 'delivered');


-- ============================================================
-- 22. SALES SUMMARY FOR DASHBOARD
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customerid) AS total_customers,
    COUNT(DISTINCT product) AS total_products,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(totalprice), 2) AS total_revenue,
    ROUND(AVG(totalprice), 2) AS average_order_value
FROM ecommerce_sales;


-- ============================================================
-- END OF SQL ANALYSIS
-- ============================================================