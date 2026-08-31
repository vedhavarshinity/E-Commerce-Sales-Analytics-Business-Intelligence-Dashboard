# 🛒 E-Commerce Sales Analytics & Business Intelligence Dashboard

# 📌 Project Overview

The E-Commerce Sales Analytics & Business Intelligence Dashboard is an end-to-end data analytics project developed to transform raw e-commerce transaction data into meaningful business insights.

The project follows a complete analytics workflow, including data preprocessing, exploratory data analysis (EDA), SQL analysis, business insights, and interactive dashboard development.

The final Streamlit dashboard provides an interactive view of sales performance, product performance, customer behavior, order status, payment methods, and referral sources.

# 🎯 Business Objective

The primary objective of this project is to help an e-commerce business understand its sales performance and customer behavior through data-driven analysis.

The project aims to answer key business questions:

How much revenue is generated?
How many orders and customers are there?
Which products generate the most revenue?
Which products have the highest sales volume?
Who are the top customers?
How do sales change over time?
What are the most commonly used payment methods?
What is the distribution of order statuses?
Which referral sources generate the most orders and revenue?
What is the average order value?

# 🎯 Project Objectives
Perform data cleaning and preprocessing.
Prepare a reliable dataset for analysis.
Conduct exploratory data analysis.
Analyze business performance using SQL.
Calculate important sales KPIs.
Identify top-performing products.
Analyze customer purchasing patterns.
Analyze order status and payment methods.
Evaluate referral source performance.
Identify monthly sales trends.
Build an interactive business intelligence dashboard.
Present actionable business insights

# 🛠️ Technologies & Tools
```
| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Python     | Data processing and analysis      |
| Pandas     | Data cleaning and manipulation    |
| NumPy      | Numerical operations              |
| Matplotlib | Visualization                     |
| Seaborn    | Statistical visualization         |
| MySQL      | SQL-based business analysis       |
| Streamlit  | Interactive dashboard             |
| Plotly     | Interactive charts                |
| Git        | Version control                   |
| GitHub     | Repository and project management |

```
# 📂 Project Structure
```
E-Commerce-Sales-Analytics-Business-Intelligence-Dashboard/
│
├── data/
│   ├── raw/
│   │   └── ecommerce_data.csv
│   │
│   └── cleaned/
│       └── ecommerce_cleaned.csv
│
├── screenshots/
│   ├── data_cleaning/
│   ├── eda/
│   ├── sql/
│   └── dashboard/
│
├── preprocessing.py
├── eda.py
├── sql_analysis.sql
├── dashboard.py
├── requirements.txt
├── README.md
└── .gitignore
```
# 📊 Dataset

The project uses an e-commerce transaction dataset containing order, customer, product, payment, and sales information.
```
| Column            | Description                               |
| ----------------- | ----------------------------------------- |
| `orderid`         | Unique identifier for each order          |
| `date`            | Date of the order                         |
| `customerid`      | Unique customer identifier                |
| `product`         | Product purchased                         |
| `quantity`        | Quantity purchased                        |
| `unitprice`       | Price per unit                            |
| `shippingaddress` | Shipping address                          |
| `paymentmethod`   | Payment method used                       |
| `orderstatus`     | Status of the order                       |
| `trackingnumber`  | Shipment tracking number                  |
| `itemsincart`     | Number of items in the cart               |
| `couponcode`      | Coupon or discount code                   |
| `referralsource`  | Source through which the customer arrived |
| `totalprice`      | Total value of the order                  |

```
# 🧹 1. Data Preprocessing

The preprocessing.py script prepares the raw dataset for analysis.

Data preprocessing includes:
```
Loading the raw CSV file.
Inspecting the dataset.
Checking missing values.
Checking duplicate records.
Handling invalid values.
Converting columns to appropriate data types.
Converting the date column to datetime format.
Converting numerical columns to numeric format.
Validating the cleaned dataset.
Exporting the cleaned dataset.
```
# 📈 2. Exploratory Data Analysis

The eda.py script performs exploratory analysis on the cleaned dataset.
```
Sales Analysis
Total revenue
Total orders
Average order value
Sales distribution
Monthly sales trends
Product Analysis
Product-wise revenue
Product-wise quantity sold
Product performance
Top-selling products
Customer Analysis
Unique customers
Customer-wise revenue
Top customers
Order Analysis
Order status distribution
Order volume
Payment Analysis
Payment method distribution
Payment performance
Referral Analysis
Referral source distribution
Orders by referral source
Revenue by referral source
```
# 🗄️ 3. SQL Business Analysis

MySQL is used to perform business-oriented analysis on the cleaned e-commerce dataset.

The SQL analysis includes:
```
Database creation
Table creation
Data loading
Total number of orders
Total revenue
Average order value
Unique customers
Unique products
Total quantity sold
Product-wise revenue
Product-wise quantity sold
Top-performing products
Customer-wise revenue
Top customers
Monthly revenue
Order status analysis
Payment method analysis
Referral source analysis
```
# 📊 4. Interactive Dashboard

The final dashboard is developed using Streamlit and Plotly.

The dashboard provides a consolidated view of e-commerce business performance.

# 🔑 Key Performance Indicators

The dashboard displays:
```
Total Orders
Unique Customers
Total Products
Total Revenue
Average Order Value
Units Sold
Successful Orders
Success Rate
```
# 🎛️ Dashboard Filters

The dashboard provides interactive filters for:

📅 Date Range
🛍️ Product
📦 Order Status
💳 Payment Method
📢 Referral Source

The KPIs, charts, and sales table update based on the selected filters.

# 📉 Dashboard Visualizations

1. Monthly Sales Trend

Shows the change in revenue over time.

2. Product Performance

Analyzes:

Revenue by product
Units sold by product

3. Order Status Distribution

Shows the proportion of orders across different order statuses.

4. Payment Method Distribution

Shows the usage of different payment methods.

5. Referral Source Analysis

Analyzes:

Revenue by referral source
Orders by referral source

6. Top Customers

Displays the top customers based on revenue generated.

7. Top Performing Products

Displays:

Number of orders
Units sold
Revenue

8. Sales Data

Displays the filtered transaction-level sales data.

9. Download Filtered Data

Users can download the filtered sales data as a CSV file.

# 💡 Business Insights

The analysis provides insights into:
```
Overall e-commerce sales performance.
Products contributing the highest revenue.
Products generating the highest sales volume.
High-value customers.
Monthly revenue patterns.
Order status distribution.
Customer payment preferences.
Performance of different referral sources.
Average order value.
Overall sales and order volume.
```
These insights can help businesses improve:
```
Product strategy
Marketing campaigns
Customer targeting
Sales planning
Revenue optimization
Business performance monitoring
```
# 📸 Screenshots

Screenshots documenting the project are organized as follows:
```
screenshots/
│
├── data_cleaning/
│
├── eda/
│
├── sql/
│
└── dashboard/
```
These folders contain screenshots of the different stages of the project, including preprocessing, EDA visualizations, SQL results, and the final dashboard.

# 📦 Project Deliverables

The project includes:
```
Raw e-commerce dataset
Cleaned dataset
Data preprocessing script
EDA script
SQL database and analysis queries
Interactive Streamlit dashboard
EDA screenshots
SQL result screenshots
Dashboard screenshots
Requirements file
Project documentation
GitHub README
```
# 🔮 Future Enhancements

The project can be further enhanced with:
```
Sales forecasting using machine learning.
Customer segmentation.
Customer Lifetime Value (CLV) analysis.
Product recommendation systems.
Customer churn prediction.
Advanced marketing analytics.
Automated business reports.
Real-time data integration.
Cloud deployment.
Predictive business intelligence.
```
# 👩‍💻 Author

Vedhavarshini T.Y.
