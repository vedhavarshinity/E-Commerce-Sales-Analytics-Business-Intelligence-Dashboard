import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# E-COMMERCE SALES DATA ANALYTICS
# COMPREHENSIVE EXPLORATORY DATA ANALYSIS
# ============================================================


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

CLEANED_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "ecommerce_cleaned.csv"
)

EDA_FOLDER = (
    BASE_DIR
    / "screenshots"
    / "eda"
)

REPORT_FOLDER = (
    EDA_FOLDER
    / "reports"
)

EDA_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# 2. HELPER FUNCTIONS
# ------------------------------------------------------------

def safe_filename(name):
    """Create a safe filename from a column name."""
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("?", "")
    )


def save_plot(filename):
    """Save the current plot."""
    filepath = EDA_FOLDER / filename

    plt.tight_layout()

    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {filepath.name}")


def find_column(columns, keywords):
    """Find a likely business column using keywords."""

    for keyword in keywords:

        for column in columns:

            if keyword in column.lower():

                return column

    return None


# ------------------------------------------------------------
# 3. LOAD CLEANED DATA
# ------------------------------------------------------------

print("=" * 70)
print("E-COMMERCE SALES DATA ANALYTICS")
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)


if not CLEANED_FILE.exists():

    raise FileNotFoundError(
        "\nCleaned dataset not found.\n"
        "Please run preprocessing.py first."
    )


df = pd.read_csv(
    CLEANED_FILE
)

print("\nCleaned dataset loaded successfully.")


# ------------------------------------------------------------
# 4. BASIC DATASET INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)

rows = df.shape[0]
columns = df.shape[1]

print(
    f"\nRows    : {rows}"
)

print(
    f"Columns : {columns}"
)

print("\nColumn Names:")

for column in df.columns:

    print(
        f"- {column}"
    )


# ------------------------------------------------------------
# 5. DATA TYPES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. DATA TYPES")
print("=" * 70)

print(
    df.dtypes
)

dtype_report = pd.DataFrame({
    "column": df.columns,
    "data_type": [
        str(df[column].dtype)
        for column in df.columns
    ]
})

dtype_report.to_csv(
    REPORT_FOLDER
    / "data_types.csv",
    index=False
)


# ------------------------------------------------------------
# 6. NUMERICAL AND CATEGORICAL COLUMNS
# ------------------------------------------------------------

numeric_columns = (
    df.select_dtypes(
        include=np.number
    )
    .columns
    .tolist()
)

categorical_columns = (
    df.select_dtypes(
        include=["object", "category"]
    )
    .columns
    .tolist()
)

print("\n" + "=" * 70)
print("3. COLUMN CLASSIFICATION")
print("=" * 70)

print("\nNumerical Columns:")

print(
    numeric_columns
)

print("\nCategorical Columns:")

print(
    categorical_columns
)


# ------------------------------------------------------------
# 7. DATASET INFORMATION REPORT
# ------------------------------------------------------------

info_report = pd.DataFrame({
    "column": df.columns,
    "data_type": [
        str(df[column].dtype)
        for column in df.columns
    ],
    "non_null": [
        df[column].notna().sum()
        for column in df.columns
    ],
    "missing": [
        df[column].isna().sum()
        for column in df.columns
    ],
    "unique": [
        df[column].nunique()
        for column in df.columns
    ]
})

info_report.to_csv(
    REPORT_FOLDER
    / "dataset_information.csv",
    index=False
)


# ------------------------------------------------------------
# 8. DESCRIPTIVE STATISTICS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. DESCRIPTIVE STATISTICS")
print("=" * 70)

if numeric_columns:

    statistics = (
        df[numeric_columns]
        .describe()
        .T
    )

    statistics["median"] = (
        df[numeric_columns]
        .median()
    )

    statistics["variance"] = (
        df[numeric_columns]
        .var()
    )

    statistics["skewness"] = (
        df[numeric_columns]
        .skew()
    )

    statistics["kurtosis"] = (
        df[numeric_columns]
        .kurt()
    )

    print(
        statistics
    )

    statistics.to_csv(
        REPORT_FOLDER
        / "descriptive_statistics.csv"
    )

else:

    print(
        "\nNo numerical columns found."
    )


# ------------------------------------------------------------
# 9. MISSING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. MISSING VALUE ANALYSIS")
print("=" * 70)

missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
)

missing_report = pd.DataFrame({
    "column": df.columns,
    "missing_count": missing_count.values,
    "missing_percentage":
        missing_percentage.values
})

missing_report = (
    missing_report
    .sort_values(
        "missing_count",
        ascending=False
    )
)

print(
    missing_report
)

missing_report.to_csv(
    REPORT_FOLDER
    / "missing_value_analysis.csv",
    index=False
)

missing_plot = missing_report[
    missing_report["missing_count"] > 0
]

if not missing_plot.empty:

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        missing_plot["column"],
        missing_plot["missing_count"]
    )

    plt.title(
        "Missing Values by Column"
    )

    plt.xlabel(
        "Column"
    )

    plt.ylabel(
        "Missing Values"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "01_missing_values.png"
    )

else:

    print(
        "\nNo missing values found."
    )


# ------------------------------------------------------------
# 10. DUPLICATE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = (
    df.duplicated().sum()
)

print(
    f"\nDuplicate Rows: "
    f"{duplicate_count}"
)

duplicate_report = pd.DataFrame({
    "metric": [
        "Duplicate Rows"
    ],
    "value": [
        duplicate_count
    ]
})

duplicate_report.to_csv(
    REPORT_FOLDER
    / "duplicate_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 11. UNIQUE VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. UNIQUE VALUE ANALYSIS")
print("=" * 70)

unique_report = pd.DataFrame({
    "column": df.columns,
    "unique_values": [
        df[column].nunique()
        for column in df.columns
    ]
})

print(
    unique_report
)

unique_report.to_csv(
    REPORT_FOLDER
    / "unique_value_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 12. MODE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. MODE ANALYSIS")
print("=" * 70)

mode_results = []

for column in df.columns:

    modes = df[column].mode(
        dropna=True
    )

    if not modes.empty:

        mode_results.append({
            "column": column,
            "mode": modes.iloc[0]
        })

mode_df = pd.DataFrame(
    mode_results
)

print(
    mode_df
)

mode_df.to_csv(
    REPORT_FOLDER
    / "mode_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 13. NUMERICAL DISTRIBUTION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. NUMERICAL DISTRIBUTION ANALYSIS")
print("=" * 70)

for column in numeric_columns:

    values = (
        df[column]
        .dropna()
    )

    if values.empty:
        continue

    plt.figure(
        figsize=(9, 5)
    )

    plt.hist(
        values,
        bins=30
    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.xlabel(
        column
    )

    plt.ylabel(
        "Frequency"
    )

    save_plot(
        f"02_distribution_{safe_filename(column)}.png"
    )


# ------------------------------------------------------------
# 14. BOX PLOT AND OUTLIER ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("10. OUTLIER ANALYSIS")
print("=" * 70)

outlier_results = []

for column in numeric_columns:

    values = (
        df[column]
        .dropna()
    )

    if len(values) < 4:
        continue

    q1 = values.quantile(
        0.25
    )

    q3 = values.quantile(
        0.75
    )

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    outliers = values[
        (values < lower_bound)
        |
        (values > upper_bound)
    ]

    outlier_count = len(
        outliers
    )

    outlier_percentage = (
        outlier_count
        / len(values)
        * 100
    )

    outlier_results.append({
        "column": column,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count":
            outlier_count,
        "outlier_percentage":
            round(
                outlier_percentage,
                2
            )
    })

    plt.figure(
        figsize=(8, 5)
    )

    plt.boxplot(
        values
    )

    plt.title(
        f"Box Plot - {column}"
    )

    plt.ylabel(
        column
    )

    save_plot(
        f"03_boxplot_{safe_filename(column)}.png"
    )


outlier_df = pd.DataFrame(
    outlier_results
)

if not outlier_df.empty:

    print(
        outlier_df
    )

    outlier_df.to_csv(
        REPORT_FOLDER
        / "outlier_analysis.csv",
        index=False
    )


# ------------------------------------------------------------
# 15. CATEGORICAL FREQUENCY ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("11. CATEGORICAL FREQUENCY ANALYSIS")
print("=" * 70)

for column in categorical_columns:

    counts = (
        df[column]
        .value_counts()
        .head(20)
    )

    print(
        f"\nTop values: {column}"
    )

    print(
        counts
    )

    counts.to_csv(
        REPORT_FOLDER
        / f"frequency_{safe_filename(column)}.csv"
    )


# ------------------------------------------------------------
# 16. CATEGORICAL VISUALIZATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("12. CATEGORICAL VISUALIZATION")
print("=" * 70)

for column in categorical_columns:

    unique_count = (
        df[column]
        .nunique()
    )

    # Avoid charts for columns containing
    # too many unique values.
    if unique_count == 0 or unique_count > 20:
        continue

    counts = (
        df[column]
        .value_counts()
        .head(20)
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title(
        f"{column} Distribution"
    )

    plt.xlabel(
        column
    )

    plt.ylabel(
        "Count"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        f"04_category_{safe_filename(column)}.png"
    )


# ------------------------------------------------------------
# 17. CORRELATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("13. CORRELATION ANALYSIS")
print("=" * 70)

if len(numeric_columns) >= 2:

    correlation = (
        df[numeric_columns]
        .corr()
    )

    print(
        correlation
    )

    correlation.to_csv(
        REPORT_FOLDER
        / "correlation_matrix.csv"
    )

    plt.figure(
        figsize=(
            max(8, len(numeric_columns)),
            max(6, len(numeric_columns))
        )
    )

    plt.imshow(
        correlation,
        interpolation="nearest"
    )

    plt.title(
        "Correlation Matrix"
    )

    plt.colorbar()

    plt.xticks(
        range(len(numeric_columns)),
        numeric_columns,
        rotation=45,
        ha="right"
    )

    plt.yticks(
        range(len(numeric_columns)),
        numeric_columns
    )

    save_plot(
        "05_correlation_matrix.png"
    )

else:

    print(
        "\nAt least two numerical "
        "columns are required."
    )


# ------------------------------------------------------------
# 18. AUTOMATIC DATE DETECTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("14. DATE/TIME ANALYSIS")
print("=" * 70)

date_columns = []

date_keywords = [
    "date",
    "time",
    "timestamp",
    "created",
    "updated",
    "ordered",
    "purchase",
    "transaction"
]

for column in df.columns:

    converted = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    original_non_null = (
        df[column]
        .notna()
        .sum()
    )

    if original_non_null == 0:
        continue

    valid_ratio = (
        converted.notna().sum()
        / original_non_null
    )

    name_signal = any(
        keyword in column.lower()
        for keyword in date_keywords
    )

    if (
        valid_ratio >= 0.70
        and name_signal
    ):

        date_columns.append(
            column
        )


print(
    "\nDetected Date Columns:"
)

print(
    date_columns
)


# ------------------------------------------------------------
# 19. DATE RANGE ANALYSIS
# ------------------------------------------------------------

for column in date_columns:

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    ).dropna()

    if dates.empty:
        continue

    print(
        f"\n{column}"
    )

    print(
        "Minimum Date:",
        dates.min()
    )

    print(
        "Maximum Date:",
        dates.max()
    )


# ------------------------------------------------------------
# 20. MONTHLY TRANSACTION TREND
# ------------------------------------------------------------

for column in date_columns:

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    ).dropna()

    if len(dates) < 2:
        continue

    monthly_count = (
        dates
        .dt.to_period("M")
        .value_counts()
        .sort_index()
    )

    if len(monthly_count) > 1:

        plt.figure(
            figsize=(11, 5)
        )

        plt.plot(
            monthly_count.index.astype(str),
            monthly_count.values,
            marker="o"
        )

        plt.title(
            f"Monthly Transaction Trend - {column}"
        )

        plt.xlabel(
            "Month"
        )

        plt.ylabel(
            "Number of Transactions"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        save_plot(
            f"06_monthly_transactions_{safe_filename(column)}.png"
        )

        monthly_count.to_csv(
            REPORT_FOLDER
            / f"monthly_transactions_{safe_filename(column)}.csv"
        )


# ------------------------------------------------------------
# 21. YEARLY TRANSACTION TREND
# ------------------------------------------------------------

for column in date_columns:

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    ).dropna()

    yearly_count = (
        dates
        .dt.year
        .value_counts()
        .sort_index()
    )

    if len(yearly_count) > 1:

        plt.figure(
            figsize=(9, 5)
        )

        plt.bar(
            yearly_count.index.astype(str),
            yearly_count.values
        )

        plt.title(
            f"Yearly Transaction Trend - {column}"
        )

        plt.xlabel(
            "Year"
        )

        plt.ylabel(
            "Number of Transactions"
        )

        save_plot(
            f"07_yearly_transactions_{safe_filename(column)}.png"
        )


# ------------------------------------------------------------
# 22. DETECT E-COMMERCE BUSINESS COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("15. E-COMMERCE BUSINESS COLUMN DETECTION")
print("=" * 70)


sales_column = find_column(
    df.columns,
    [
        "sales",
        "revenue",
        "amount",
        "total_sales",
        "turnover"
    ]
)


quantity_column = find_column(
    df.columns,
    [
        "quantity",
        "qty",
        "units"
    ]
)


price_column = find_column(
    df.columns,
    [
        "price",
        "unit_price",
        "selling_price"
    ]
)


product_column = find_column(
    df.columns,
    [
        "product_name",
        "product",
        "item_name",
        "item"
    ]
)


category_column = find_column(
    df.columns,
    [
        "category",
        "product_category",
        "subcategory"
    ]
)


customer_column = find_column(
    df.columns,
    [
        "customer_id",
        "customer_name",
        "customer",
        "buyer"
    ]
)


print(
    "\nDetected Business Columns:"
)

print(
    "Sales    :", sales_column
)

print(
    "Quantity :", quantity_column
)

print(
    "Price    :", price_column
)

print(
    "Product  :", product_column
)

print(
    "Category :", category_column
)

print(
    "Customer :", customer_column
)


# ------------------------------------------------------------
# 23. SALES / REVENUE ANALYSIS
# ------------------------------------------------------------

if sales_column:

    print("\n" + "=" * 70)
    print("16. SALES / REVENUE ANALYSIS")
    print("=" * 70)

    total_sales = (
        df[sales_column].sum()
    )

    average_sales = (
        df[sales_column].mean()
    )

    median_sales = (
        df[sales_column].median()
    )

    print(
        f"\nTotal Sales/Revenue: "
        f"{total_sales:,.2f}"
    )

    print(
        f"Average Sales: "
        f"{average_sales:,.2f}"
    )

    print(
        f"Median Sales: "
        f"{median_sales:,.2f}"
    )


# ------------------------------------------------------------
# 24. TOP PRODUCTS BY SALES
# ------------------------------------------------------------

if sales_column and product_column:

    product_sales = (
        df.groupby(
            product_column
        )[sales_column]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print(
        "\nTop 10 Products by Sales:"
    )

    print(
        product_sales
    )

    product_sales.to_csv(
        REPORT_FOLDER
        / "top_products_by_sales.csv"
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        product_sales.index.astype(str),
        product_sales.values
    )

    plt.title(
        "Top 10 Products by Sales"
    )

    plt.xlabel(
        "Product"
    )

    plt.ylabel(
        "Sales"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "08_top_products_by_sales.png"
    )


# ------------------------------------------------------------
# 25. SALES BY CATEGORY
# ------------------------------------------------------------

if sales_column and category_column:

    category_sales = (
        df.groupby(
            category_column
        )[sales_column]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        "\nSales by Category:"
    )

    print(
        category_sales
    )

    category_sales.to_csv(
        REPORT_FOLDER
        / "sales_by_category.csv"
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        category_sales.index.astype(str),
        category_sales.values
    )

    plt.title(
        "Sales by Category"
    )

    plt.xlabel(
        "Category"
    )

    plt.ylabel(
        "Sales"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "09_sales_by_category.png"
    )


# ------------------------------------------------------------
# 26. QUANTITY ANALYSIS
# ------------------------------------------------------------

if quantity_column:

    print("\n" + "=" * 70)
    print("17. QUANTITY ANALYSIS")
    print("=" * 70)

    total_quantity = (
        df[quantity_column].sum()
    )

    average_quantity = (
        df[quantity_column].mean()
    )

    print(
        f"\nTotal Quantity Sold: "
        f"{total_quantity:,.2f}"
    )

    print(
        f"Average Quantity: "
        f"{average_quantity:,.2f}"
    )


# ------------------------------------------------------------
# 27. TOP PRODUCTS BY QUANTITY
# ------------------------------------------------------------

if quantity_column and product_column:

    product_quantity = (
        df.groupby(
            product_column
        )[quantity_column]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print(
        "\nTop 10 Products by Quantity:"
    )

    print(
        product_quantity
    )

    product_quantity.to_csv(
        REPORT_FOLDER
        / "top_products_by_quantity.csv"
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        product_quantity.index.astype(str),
        product_quantity.values
    )

    plt.title(
        "Top 10 Products by Quantity Sold"
    )

    plt.xlabel(
        "Product"
    )

    plt.ylabel(
        "Quantity"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "10_top_products_by_quantity.png"
    )


# ------------------------------------------------------------
# 28. CUSTOMER ANALYSIS
# ------------------------------------------------------------

if customer_column:

    print("\n" + "=" * 70)
    print("18. CUSTOMER ANALYSIS")
    print("=" * 70)

    unique_customers = (
        df[customer_column]
        .nunique()
    )

    print(
        f"\nUnique Customers: "
        f"{unique_customers:,}"
    )


# ------------------------------------------------------------
# 29. TOP CUSTOMERS BY SALES
# ------------------------------------------------------------

if customer_column and sales_column:

    customer_sales = (
        df.groupby(
            customer_column
        )[sales_column]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print(
        "\nTop 10 Customers by Sales:"
    )

    print(
        customer_sales
    )

    customer_sales.to_csv(
        REPORT_FOLDER
        / "top_customers_by_sales.csv"
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        customer_sales.index.astype(str),
        customer_sales.values
    )

    plt.title(
        "Top 10 Customers by Sales"
    )

    plt.xlabel(
        "Customer"
    )

    plt.ylabel(
        "Sales"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_plot(
        "11_top_customers_by_sales.png"
    )


# ------------------------------------------------------------
# 30. PRICE ANALYSIS
# ------------------------------------------------------------

if price_column:

    print("\n" + "=" * 70)
    print("19. PRICE ANALYSIS")
    print("=" * 70)

    print(
        "\nAverage Price:",
        round(
            df[price_column].mean(),
            2
        )
    )

    print(
        "Minimum Price:",
        df[price_column].min()
    )

    print(
        "Maximum Price:",
        df[price_column].max()
    )

    plt.figure(
        figsize=(9, 5)
    )

    plt.hist(
        df[price_column].dropna(),
        bins=30
    )

    plt.title(
        "Price Distribution"
    )

    plt.xlabel(
        "Price"
    )

    plt.ylabel(
        "Frequency"
    )

    save_plot(
        "12_price_distribution.png"
    )


# ------------------------------------------------------------
# 31. SALES VS QUANTITY
# ------------------------------------------------------------

if sales_column and quantity_column:

    plt.figure(
        figsize=(9, 6)
    )

    plt.scatter(
        df[quantity_column],
        df[sales_column],
        alpha=0.6
    )

    plt.title(
        "Sales vs Quantity"
    )

    plt.xlabel(
        "Quantity"
    )

    plt.ylabel(
        "Sales"
    )

    save_plot(
        "13_sales_vs_quantity.png"
    )


# ------------------------------------------------------------
# 32. PRICE VS SALES
# ------------------------------------------------------------

if sales_column and price_column:

    plt.figure(
        figsize=(9, 6)
    )

    plt.scatter(
        df[price_column],
        df[sales_column],
        alpha=0.6
    )

    plt.title(
        "Price vs Sales"
    )

    plt.xlabel(
        "Price"
    )

    plt.ylabel(
        "Sales"
    )

    save_plot(
        "14_price_vs_sales.png"
    )


# ------------------------------------------------------------
# 33. MONTHLY SALES TREND
# ------------------------------------------------------------

if sales_column and date_columns:

    for date_column in date_columns:

        temp = df.copy()

        temp[date_column] = (
            pd.to_datetime(
                temp[date_column],
                errors="coerce"
            )
        )

        temp = temp.dropna(
            subset=[
                date_column,
                sales_column
            ]
        )

        if len(temp) < 2:
            continue

        monthly_sales = (
            temp
            .set_index(date_column)
            [sales_column]
            .resample("ME")
            .sum()
        )

        if len(monthly_sales) > 1:

            plt.figure(
                figsize=(11, 5)
            )

            plt.plot(
                monthly_sales.index,
                monthly_sales.values,
                marker="o"
            )

            plt.title(
                f"Monthly Sales Trend - {date_column}"
            )

            plt.xlabel(
                "Date"
            )

            plt.ylabel(
                "Sales"
            )

            plt.xticks(
                rotation=45,
                ha="right"
            )

            save_plot(
                "15_monthly_sales_trend.png"
            )

            monthly_sales.to_csv(
                REPORT_FOLDER
                / "monthly_sales.csv"
            )


# ------------------------------------------------------------
# 34. CATEGORY DISTRIBUTION
# ------------------------------------------------------------

if category_column:

    category_count = (
        df[category_column]
        .value_counts()
    )

    if (
        len(category_count) > 0
        and len(category_count) <= 15
    ):

        plt.figure(
            figsize=(8, 8)
        )

        plt.pie(
            category_count.values,
            labels=category_count.index.astype(str),
            autopct="%1.1f%%"
        )

        plt.title(
            "Category Distribution"
        )

        save_plot(
            "16_category_distribution.png"
        )


# ------------------------------------------------------------
# 35. CUSTOMER ORDER FREQUENCY
# ------------------------------------------------------------

if customer_column:

    customer_frequency = (
        df[customer_column]
        .value_counts()
        .head(10)
    )

    print(
        "\nTop Customers by Number of Orders:"
    )

    print(
        customer_frequency
    )

    customer_frequency.to_csv(
        REPORT_FOLDER
        / "customer_order_frequency.csv"
    )


# ------------------------------------------------------------
# 36. AUTOMATIC BUSINESS INSIGHTS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("20. BUSINESS INSIGHTS")
print("=" * 70)

insights = []


# Dataset insight

insights.append(
    f"The dataset contains {rows:,} records "
    f"and {columns} columns."
)


# Missing values

total_missing = int(
    df.isnull().sum().sum()
)

if total_missing == 0:

    insights.append(
        "The cleaned dataset contains no "
        "missing values."
    )

else:

    insights.append(
        f"The dataset contains "
        f"{total_missing:,} missing values."
    )


# Duplicate insight

if duplicate_count == 0:

    insights.append(
        "No duplicate records were identified."
    )

else:

    insights.append(
        f"{duplicate_count:,} duplicate records "
        "were identified."
    )


# Sales insight

if sales_column:

    total_sales = (
        df[sales_column].sum()
    )

    insights.append(
        f"Total sales/revenue is "
        f"{total_sales:,.2f}."
    )

    if product_column:

        product_sales_all = (
            df.groupby(
                product_column
            )[sales_column]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not product_sales_all.empty:

            top_product = (
                product_sales_all
                .index[0]
            )

            top_product_sales = (
                product_sales_all
                .iloc[0]
            )

            insights.append(
                f"The highest-sales product is "
                f"'{top_product}' with sales of "
                f"{top_product_sales:,.2f}."
            )


# Category insight

if sales_column and category_column:

    category_sales_all = (
        df.groupby(
            category_column
        )[sales_column]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if not category_sales_all.empty:

        top_category = (
            category_sales_all
            .index[0]
        )

        top_category_sales = (
            category_sales_all
            .iloc[0]
        )

        insights.append(
            f"The highest-performing category is "
            f"'{top_category}' with sales of "
            f"{top_category_sales:,.2f}."
        )


# Customer insight

if customer_column:

    customer_count = (
        df[customer_column]
        .nunique()
    )

    insights.append(
        f"The dataset contains "
        f"{customer_count:,} unique customers."
    )


# Quantity insight

if quantity_column:

    total_quantity = (
        df[quantity_column].sum()
    )

    insights.append(
        f"Total quantity sold is "
        f"{total_quantity:,.2f}."
    )


for number, insight in enumerate(
    insights,
    start=1
):

    print(
        f"{number}. {insight}"
    )


# ------------------------------------------------------------
# 37. SAVE BUSINESS INSIGHTS
# ------------------------------------------------------------

with open(
    REPORT_FOLDER
    / "business_insights.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "E-COMMERCE BUSINESS INSIGHTS\n"
    )

    file.write(
        "=" * 70
        + "\n\n"
    )

    for number, insight in enumerate(
        insights,
        start=1
    ):

        file.write(
            f"{number}. {insight}\n"
        )


# ------------------------------------------------------------
# 38. FINAL EDA SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL EDA SUMMARY")
print("=" * 70)

print(
    f"\nDataset Size:"
    f" {rows:,} rows × {columns} columns"
)

print(
    f"Numerical Columns:"
    f" {len(numeric_columns)}"
)

print(
    f"Categorical Columns:"
    f" {len(categorical_columns)}"
)

print(
    f"Date Columns:"
    f" {len(date_columns)}"
)

print(
    f"Duplicate Rows:"
    f" {duplicate_count:,}"
)

print(
    f"Missing Values:"
    f" {total_missing:,}"
)

print(
    "\nEDA outputs saved to:"
)

print(
    EDA_FOLDER
)

print(
    "\nEDA completed successfully!"
)

print("=" * 70)