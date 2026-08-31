import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# E-COMMERCE SALES DATA ANALYTICS
# COMPLETE DATA PREPROCESSING
# ============================================================


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

RAW_FILE = BASE_DIR / "data" / "raw" / "ecommerce_data.csv"

CLEANED_DIR = BASE_DIR / "data" / "cleaned"

CLEANED_FILE = (
    CLEANED_DIR / "ecommerce_cleaned.csv"
)

SCREENSHOT_DIR = (
    BASE_DIR / "screenshots" / "data_cleaning"
)

REPORT_DIR = (
    SCREENSHOT_DIR / "reports"
)

CLEANED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

SCREENSHOT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# 2. LOAD RAW DATASET
# ------------------------------------------------------------

print("=" * 70)
print("E-COMMERCE SALES DATA ANALYTICS")
print("DATA PREPROCESSING")
print("=" * 70)

if not RAW_FILE.exists():

    raise FileNotFoundError(
        "\nRaw dataset not found!\n\n"
        f"Expected location:\n{RAW_FILE}\n\n"
        "Please place ecommerce_raw.csv inside:\n"
        "data/raw/"
    )


df = pd.read_csv(RAW_FILE)

print("\nDataset loaded successfully.")


# ------------------------------------------------------------
# 3. STORE INITIAL INFORMATION
# ------------------------------------------------------------

initial_rows = len(df)
initial_columns = len(df.columns)

initial_missing = int(
    df.isnull().sum().sum()
)

initial_duplicates = int(
    df.duplicated().sum()
)


# ------------------------------------------------------------
# 4. INITIAL DATASET INSPECTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. INITIAL DATASET INSPECTION")
print("=" * 70)

print(
    f"\nRows    : {initial_rows}"
)

print(
    f"Columns : {initial_columns}"
)

print("\nColumns:")

for column in df.columns:
    print(f"- {column}")

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print(
    f"\nDuplicate Rows: {initial_duplicates}"
)


# ------------------------------------------------------------
# 5. CLEAN COLUMN NAMES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. CLEANING COLUMN NAMES")
print("=" * 70)

old_columns = df.columns.tolist()

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace("/", "_", regex=False)
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

print("\nColumn names standardized.")

print("\nBefore:")

for column in old_columns:
    print(f"- {column}")

print("\nAfter:")

for column in df.columns:
    print(f"- {column}")


# ------------------------------------------------------------
# 6. REMOVE COMPLETELY EMPTY ROWS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. REMOVING COMPLETELY EMPTY ROWS")
print("=" * 70)

rows_before_empty = len(df)

df = df.dropna(
    axis=0,
    how="all"
)

rows_removed_empty = (
    rows_before_empty - len(df)
)

print(
    f"\nCompletely empty rows removed: "
    f"{rows_removed_empty}"
)


# ------------------------------------------------------------
# 7. REMOVE COMPLETELY EMPTY COLUMNS
# ------------------------------------------------------------

columns_before_empty = len(df.columns)

df = df.dropna(
    axis=1,
    how="all"
)

columns_removed_empty = (
    columns_before_empty - len(df.columns)
)

print(
    f"Completely empty columns removed: "
    f"{columns_removed_empty}"
)


# ------------------------------------------------------------
# 8. STANDARDIZE MISSING VALUE REPRESENTATIONS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. STANDARDIZING MISSING VALUES")
print("=" * 70)

missing_representations = [
    "",
    " ",
    "NA",
    "N/A",
    "na",
    "n/a",
    "NULL",
    "null",
    "None",
    "none",
    "missing",
    "Missing",
    "-",
    "--"
]

df = df.replace(
    missing_representations,
    np.nan
)

print(
    "\nMissing-value representations "
    "standardized to NaN."
)


# ------------------------------------------------------------
# 9. REMOVE DUPLICATE RECORDS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. DUPLICATE RECORD REMOVAL")
print("=" * 70)

duplicates_before = df.duplicated().sum()

if duplicates_before > 0:

    df = df.drop_duplicates()

    print(
        f"\nRemoved {duplicates_before} "
        "duplicate rows."
    )

else:

    print("\nNo duplicate records found.")


# ------------------------------------------------------------
# 10. CLEAN TEXT COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. TEXT DATA CLEANING")
print("=" * 70)

text_columns = (
    df.select_dtypes(
        include=["object"]
    ).columns
)

for column in text_columns:

    # Convert values to string only where
    # values are not missing.
    df[column] = df[column].apply(
        lambda value:
        value.strip()
        if isinstance(value, str)
        else value
    )

    print(
        f"Cleaned text: {column}"
    )


# ------------------------------------------------------------
# 11. STANDARDIZE CATEGORICAL TEXT
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. STANDARDIZING CATEGORICAL VALUES")
print("=" * 70)

for column in text_columns:

    unique_count = df[column].nunique(
        dropna=True
    )

    # Apply case standardization only to columns
    # with a relatively small number of categories.
    if 1 < unique_count <= 50:

        df[column] = df[column].apply(
            lambda value:
            value.title()
            if isinstance(value, str)
            else value
        )

        print(
            f"Standardized categories: {column}"
        )


# ------------------------------------------------------------
# 12. CONVERT NUMERIC-LOOKING COLUMNS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. NUMERICAL DATA TYPE CONVERSION")
print("=" * 70)

numeric_conversion_report = []

for column in df.columns:

    if df[column].dtype != "object":
        continue

    non_null = df[column].notna().sum()

    if non_null == 0:
        continue

    cleaned_values = (
        df[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("£", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    converted = pd.to_numeric(
        cleaned_values,
        errors="coerce"
    )

    valid_numeric = converted.notna().sum()

    ratio = (
        valid_numeric / non_null
    )

    if ratio >= 0.80:

        df[column] = converted

        numeric_conversion_report.append(
            column
        )

        print(
            f"Converted to numeric: {column}"
        )


# ------------------------------------------------------------
# 13. DATE COLUMN DETECTION AND CONVERSION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. DATE DATA TYPE CONVERSION")
print("=" * 70)

date_columns = []

date_keywords = [
    "date",
    "time",
    "timestamp",
    "created",
    "updated",
    "ordered",
    "purchase"
]

for column in df.columns:

    # Strong signal from column name
    name_signal = any(
        keyword in column.lower()
        for keyword in date_keywords
    )

    if name_signal:

        converted = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        non_null = df[column].notna().sum()

        if non_null > 0:

            valid_dates = converted.notna().sum()

            ratio = (
                valid_dates / non_null
            )

            if ratio >= 0.70:

                df[column] = converted

                date_columns.append(
                    column
                )

                print(
                    f"Converted to datetime: "
                    f"{column}"
                )


# ------------------------------------------------------------
# 14. HANDLE MISSING NUMERICAL VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("10. HANDLING MISSING NUMERICAL VALUES")
print("=" * 70)

numeric_columns = (
    df.select_dtypes(
        include=np.number
    ).columns.tolist()
)

missing_numeric_report = []

for column in numeric_columns:

    missing_count = df[column].isnull().sum()

    if missing_count == 0:
        continue

    median_value = df[column].median()

    if pd.notna(median_value):

        df[column] = (
            df[column]
            .fillna(median_value)
        )

        missing_numeric_report.append({
            "column": column,
            "missing_values": missing_count,
            "method": "Median",
            "replacement_value": median_value
        })

        print(
            f"{column}: {missing_count} "
            f"values filled using median."
        )


# ------------------------------------------------------------
# 15. HANDLE MISSING CATEGORICAL VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("11. HANDLING MISSING CATEGORICAL VALUES")
print("=" * 70)

categorical_columns = (
    df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
)

missing_categorical_report = []

for column in categorical_columns:

    missing_count = df[column].isnull().sum()

    if missing_count == 0:
        continue

    mode_values = df[column].mode(
        dropna=True
    )

    if not mode_values.empty:

        mode_value = mode_values.iloc[0]

        df[column] = (
            df[column]
            .fillna(mode_value)
        )

        missing_categorical_report.append({
            "column": column,
            "missing_values": missing_count,
            "method": "Mode",
            "replacement_value": mode_value
        })

        print(
            f"{column}: {missing_count} "
            f"values filled using mode."
        )


# ------------------------------------------------------------
# 16. HANDLE MISSING DATE VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("12. DATE VALUE VALIDATION")
print("=" * 70)

for column in date_columns:

    missing_count = (
        df[column].isnull().sum()
    )

    if missing_count > 0:

        print(
            f"{column}: {missing_count} "
            "invalid/missing dates remain."
        )

    else:

        print(
            f"{column}: No missing dates."
        )


# ------------------------------------------------------------
# 17. NUMERICAL VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("13. NUMERICAL DATA VALIDATION")
print("=" * 70)

invalid_numeric_report = []

for column in numeric_columns:

    negative_count = (
        df[column] < 0
    ).sum()

    zero_count = (
        df[column] == 0
    ).sum()

    print(
        f"\n{column}"
    )

    print(
        f"Negative values: {negative_count}"
    )

    print(
        f"Zero values: {zero_count}"
    )

    if negative_count > 0:

        invalid_numeric_report.append({
            "column": column,
            "negative_values": int(
                negative_count
            )
        })


# ------------------------------------------------------------
# 18. BUSINESS NUMERIC COLUMN VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("14. BUSINESS VALUE VALIDATION")
print("=" * 70)

business_keywords = {
    "quantity": [
        "quantity",
        "qty",
        "units"
    ],
    "price": [
        "price",
        "unit_price",
        "selling_price"
    ],
    "sales": [
        "sales",
        "revenue",
        "amount",
        "total"
    ]
}

for business_type, keywords in business_keywords.items():

    for column in numeric_columns:

        if any(
            keyword in column.lower()
            for keyword in keywords
        ):

            negative_values = (
                df[column] < 0
            ).sum()

            if negative_values > 0:

                print(
                    f"{column}: "
                    f"{negative_values} negative "
                    f"{business_type} values found."
                )

                # Replace invalid negative values
                # with NaN.
                df.loc[
                    df[column] < 0,
                    column
                ] = np.nan

                median_value = (
                    df[column].median()
                )

                if pd.notna(median_value):

                    df[column] = (
                        df[column]
                        .fillna(median_value)
                    )

                    print(
                        f"Invalid values replaced "
                        f"using median."
                    )

            else:

                print(
                    f"{column}: No negative "
                    f"{business_type} values."
                )


# ------------------------------------------------------------
# 19. DATE RANGE VALIDATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("15. DATE RANGE VALIDATION")
print("=" * 70)

for column in date_columns:

    valid_dates = df[column].dropna()

    if len(valid_dates) == 0:
        continue

    print(
        f"\n{column}"
    )

    print(
        "Minimum Date:",
        valid_dates.min()
    )

    print(
        "Maximum Date:",
        valid_dates.max()
    )


# ------------------------------------------------------------
# 20. OUTLIER DETECTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("16. OUTLIER DETECTION")
print("=" * 70)

outlier_results = []

for column in numeric_columns:

    values = df[column].dropna()

    if len(values) < 4:
        continue

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    outliers = values[
        (values < lower_bound)
        | (values > upper_bound)
    ]

    outlier_count = len(outliers)

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
        "outlier_count": outlier_count,
        "outlier_percentage":
            round(
                outlier_percentage,
                2
            )
    })

    print(
        f"\n{column}: "
        f"{outlier_count} outliers "
        f"({outlier_percentage:.2f}%)"
    )


outlier_df = pd.DataFrame(
    outlier_results
)

if not outlier_df.empty:

    outlier_df.to_csv(
        REPORT_DIR
        / "outlier_analysis.csv",
        index=False
    )


# ------------------------------------------------------------
# 21. FINAL MISSING VALUE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("17. FINAL MISSING VALUE CHECK")
print("=" * 70)

final_missing = df.isnull().sum()

print(
    final_missing
)

total_final_missing = int(
    final_missing.sum()
)


# ------------------------------------------------------------
# 22. FINAL DUPLICATE CHECK
# ------------------------------------------------------------

final_duplicates = int(
    df.duplicated().sum()
)

print(
    f"\nFinal Duplicate Rows: "
    f"{final_duplicates}"
)


# ------------------------------------------------------------
# 23. RESET INDEX
# ------------------------------------------------------------

df = df.reset_index(
    drop=True
)


# ------------------------------------------------------------
# 24. SAVE CLEANED DATASET
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("18. SAVING CLEANED DATASET")
print("=" * 70)

df.to_csv(
    CLEANED_FILE,
    index=False
)

print(
    f"\nCleaned dataset saved to:\n"
    f"{CLEANED_FILE}"
)


# ------------------------------------------------------------
# 25. CREATE PREPROCESSING REPORT
# ------------------------------------------------------------

final_rows = len(df)
final_columns = len(df.columns)

report = {
    "Initial Rows": initial_rows,
    "Final Rows": final_rows,
    "Rows Removed": initial_rows - final_rows,

    "Initial Columns": initial_columns,
    "Final Columns": final_columns,
    "Columns Removed":
        initial_columns - final_columns,

    "Initial Missing Values":
        initial_missing,

    "Final Missing Values":
        total_final_missing,

    "Initial Duplicate Rows":
        initial_duplicates,

    "Final Duplicate Rows":
        final_duplicates,

    "Numerical Columns":
        len(numeric_columns),

    "Categorical Columns":
        len(categorical_columns),

    "Date Columns":
        len(date_columns),

    "Outlier Columns":
        len(outlier_results)
}


report_df = pd.DataFrame(
    list(report.items()),
    columns=[
        "Metric",
        "Value"
    ]
)

report_df.to_csv(
    REPORT_DIR
    / "preprocessing_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 26. SAVE COLUMN INFORMATION
# ------------------------------------------------------------

column_information = pd.DataFrame({
    "column": df.columns,
    "data_type": [
        str(df[column].dtype)
        for column in df.columns
    ],
    "non_null_values": [
        df[column].notna().sum()
        for column in df.columns
    ],
    "missing_values": [
        df[column].isnull().sum()
        for column in df.columns
    ],
    "unique_values": [
        df[column].nunique()
        for column in df.columns
    ]
})

column_information.to_csv(
    REPORT_DIR
    / "column_information.csv",
    index=False
)


# ------------------------------------------------------------
# 27. SAVE DATA PREVIEW
# ------------------------------------------------------------

df.head(20).to_csv(
    REPORT_DIR
    / "cleaned_data_preview.csv",
    index=False
)


# ------------------------------------------------------------
# 28. FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PREPROCESSING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nInitial Dataset : "
    f"{initial_rows} rows × "
    f"{initial_columns} columns"
)

print(
    f"Final Dataset   : "
    f"{final_rows} rows × "
    f"{final_columns} columns"
)

print(
    f"Missing Values  : "
    f"{total_final_missing}"
)

print(
    f"Duplicates      : "
    f"{final_duplicates}"
)

print(
    f"Numerical       : "
    f"{len(numeric_columns)}"
)

print(
    f"Categorical     : "
    f"{len(categorical_columns)}"
)

print(
    f"Date Columns    : "
    f"{len(date_columns)}"
)

print(
    f"Outlier Checks  : "
    f"{len(outlier_results)} columns"
)

print(
    "\nCleaned Dataset:"
)

print(
    CLEANED_FILE
)

print(
    "\nPreprocessing Reports:"
)

print(
    REPORT_DIR
)

print("\n" + "=" * 70)