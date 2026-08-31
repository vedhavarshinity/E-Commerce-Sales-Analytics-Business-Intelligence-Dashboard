import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=" E-Commerce-Sales-Analytics-Business-Intelligence-Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 17px;
        color: #666666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "ecommerce_cleaned.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    if not DATA_PATH.exists():

        st.error(
            f"Dataset not found:\n{DATA_PATH}"
        )

        st.stop()

    data = pd.read_csv(DATA_PATH)

    # Clean column names
    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------------
    # Convert DATE
    # --------------------------------------------------------

    if "date" in data.columns:

        data["date"] = pd.to_datetime(
            data["date"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Convert numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "quantity",
        "unitprice",
        "itemsincart",
        "totalprice"
    ]

    for column in numeric_columns:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    # Remove rows without valid date
    if "date" in data.columns:

        data = data.dropna(
            subset=["date"]
        )

    # Remove rows without valid revenue
    if "totalprice" in data.columns:

        data = data.dropna(
            subset=["totalprice"]
        )

    # --------------------------------------------------------
    # Create date fields
    # --------------------------------------------------------

    if "date" in data.columns:

        data["year"] = data["date"].dt.year

        data["month"] = data["date"].dt.month

        data["year_month"] = (
            data["date"]
            .dt.to_period("M")
            .astype(str)
        )

    return data


df = load_data()


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🛒  E-Commerce-Sales-Analytics-Business-Intelligence-Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Interactive analysis of sales, customers, products and business performance'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔎 Filters")

st.sidebar.markdown("---")


# ============================================================
# DATE FILTER
# ============================================================

if "date" in df.columns:

    minimum_date = df["date"].min().date()
    maximum_date = df["date"].max().date()

    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date
    )

    if len(date_range) == 2:

        start_date = pd.Timestamp(
            date_range[0]
        )

        end_date = (
            pd.Timestamp(date_range[1])
            + pd.Timedelta(days=1)
        )

        filtered_df = df[
            (df["date"] >= start_date)
            &
            (df["date"] < end_date)
        ].copy()

    else:

        filtered_df = df.copy()

else:

    filtered_df = df.copy()


# ============================================================
# PRODUCT FILTER
# ============================================================

if "product" in df.columns:

    product_list = sorted(
        df["product"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_products = st.sidebar.multiselect(
        "🛍️ Product",
        product_list,
        default=product_list
    )

    if selected_products:

        filtered_df = filtered_df[
            filtered_df["product"].isin(
                selected_products
            )
        ]


# ============================================================
# ORDER STATUS FILTER
# ============================================================

if "orderstatus" in df.columns:

    status_list = sorted(
        df["orderstatus"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_status = st.sidebar.multiselect(
        "📦 Order Status",
        status_list,
        default=status_list
    )

    if selected_status:

        filtered_df = filtered_df[
            filtered_df["orderstatus"].isin(
                selected_status
            )
        ]


# ============================================================
# PAYMENT METHOD FILTER
# ============================================================

if "paymentmethod" in df.columns:

    payment_list = sorted(
        df["paymentmethod"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_payment = st.sidebar.multiselect(
        "💳 Payment Method",
        payment_list,
        default=payment_list
    )

    if selected_payment:

        filtered_df = filtered_df[
            filtered_df["paymentmethod"].isin(
                selected_payment
            )
        ]


# ============================================================
# REFERRAL SOURCE FILTER
# ============================================================

if "referralsource" in df.columns:

    referral_list = sorted(
        df["referralsource"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_referral = st.sidebar.multiselect(
        "📢 Referral Source",
        referral_list,
        default=referral_list
    )

    if selected_referral:

        filtered_df = filtered_df[
            filtered_df["referralsource"].isin(
                selected_referral
            )
        ]


# ============================================================
# NO DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No records found for the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = len(filtered_df)

total_customers = (
    filtered_df["customerid"].nunique()
    if "customerid" in filtered_df.columns
    else 0
)

total_products = (
    filtered_df["product"].nunique()
    if "product" in filtered_df.columns
    else 0
)

total_units = (
    filtered_df["quantity"].sum()
    if "quantity" in filtered_df.columns
    else 0
)

total_revenue = (
    filtered_df["totalprice"].sum()
    if "totalprice" in filtered_df.columns
    else 0
)

average_order_value = (
    filtered_df["totalprice"].mean()
    if "totalprice" in filtered_df.columns
    else 0
)


# ============================================================
# BUSINESS OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Business Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col2:

    st.metric(
        "Unique Customers",
        f"{total_customers:,}"
    )


with col3:

    st.metric(
        "Products",
        f"{total_products:,}"
    )


with col4:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )


with col5:

    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.2f}"
    )


# ============================================================
# SECOND KPI ROW
# ============================================================

st.markdown("")


col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# UNITS SOLD
# ------------------------------------------------------------

with col1:

    st.metric(
        "📦 Units Sold",
        f"{total_units:,.0f}"
    )


# ------------------------------------------------------------
# SUCCESSFUL ORDERS
# ------------------------------------------------------------

if "orderstatus" in filtered_df.columns:

    successful_orders = (
        filtered_df["orderstatus"]
        .astype(str)
        .str.lower()
        .isin(
            ["completed", "delivered", "shipped"]
        )
        .sum()
    )

else:

    successful_orders = 0


with col2:

    st.metric(
        "✅ Successful Orders",
        f"{successful_orders:,}"
    )


# ------------------------------------------------------------
# SUCCESS RATE
# ------------------------------------------------------------

if total_orders > 0:

    success_rate = (
        successful_orders / total_orders
    ) * 100

else:

    success_rate = 0


with col3:

    st.metric(
        "📈 Success Rate",
        f"{success_rate:.2f}%"
    )


# ============================================================
# MONTHLY SALES
# ============================================================

st.markdown(
    '<div class="section-title">📈 Monthly Sales Trend</div>',
    unsafe_allow_html=True
)


if "date" in filtered_df.columns:

    monthly_sales = (
        filtered_df
        .groupby("year_month", as_index=False)
        .agg(
            Revenue=("totalprice", "sum"),
            Orders=("orderid", "count")
        )
        .sort_values("year_month")
    )

    fig_monthly = px.line(
        monthly_sales,
        x="year_month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">🛍️ Product Performance</div>',
    unsafe_allow_html=True
)


if "product" in filtered_df.columns:

    product_data = (
        filtered_df
        .groupby("product", as_index=False)
        .agg(
            Revenue=("totalprice", "sum"),
            Units_Sold=("quantity", "sum"),
            Orders=("orderid", "count")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # REVENUE BY PRODUCT
    # --------------------------------------------------------

    with col1:

        fig_product_revenue = px.bar(
            product_data,
            x="product",
            y="Revenue",
            title="Revenue by Product"
        )

        fig_product_revenue.update_layout(
            xaxis_title="Product",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_product_revenue,
            use_container_width=True
        )


    # --------------------------------------------------------
    # UNITS BY PRODUCT
    # --------------------------------------------------------

    with col2:

        fig_product_units = px.bar(
            product_data,
            x="product",
            y="Units_Sold",
            title="Units Sold by Product"
        )

        fig_product_units.update_layout(
            xaxis_title="Product",
            yaxis_title="Units Sold"
        )

        st.plotly_chart(
            fig_product_units,
            use_container_width=True
        )


# ============================================================
# ORDER STATUS & PAYMENT
# ============================================================

st.markdown(
    '<div class="section-title">📦 Order & Payment Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# ORDER STATUS
# ------------------------------------------------------------

with col1:

    if "orderstatus" in filtered_df.columns:

        status_data = (
            filtered_df["orderstatus"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "Status",
            "Orders"
        ]

        fig_status = px.pie(
            status_data,
            names="Status",
            values="Orders",
            hole=0.45,
            title="Order Status Distribution"
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )


# ------------------------------------------------------------
# PAYMENT METHOD
# ------------------------------------------------------------

with col2:

    if "paymentmethod" in filtered_df.columns:

        payment_data = (
            filtered_df["paymentmethod"]
            .value_counts()
            .reset_index()
        )

        payment_data.columns = [
            "Payment Method",
            "Orders"
        ]

        fig_payment = px.pie(
            payment_data,
            names="Payment Method",
            values="Orders",
            hole=0.45,
            title="Payment Method Distribution"
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )


# ============================================================
# REFERRAL SOURCE
# ============================================================

st.markdown(
    '<div class="section-title">📢 Referral Source Analysis</div>',
    unsafe_allow_html=True
)


if "referralsource" in filtered_df.columns:

    referral_data = (
        filtered_df
        .groupby("referralsource", as_index=False)
        .agg(
            Revenue=("totalprice", "sum"),
            Orders=("orderid", "count")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # REFERRAL REVENUE
    # --------------------------------------------------------

    with col1:

        fig_referral_revenue = px.bar(
            referral_data,
            x="referralsource",
            y="Revenue",
            title="Revenue by Referral Source"
        )

        fig_referral_revenue.update_layout(
            xaxis_title="Referral Source",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_referral_revenue,
            use_container_width=True
        )


    # --------------------------------------------------------
    # REFERRAL ORDERS
    # --------------------------------------------------------

    with col2:

        fig_referral_orders = px.bar(
            referral_data,
            x="referralsource",
            y="Orders",
            title="Orders by Referral Source"
        )

        fig_referral_orders.update_layout(
            xaxis_title="Referral Source",
            yaxis_title="Orders"
        )

        st.plotly_chart(
            fig_referral_orders,
            use_container_width=True
        )


# ============================================================
# TOP CUSTOMERS
# ============================================================

st.markdown(
    '<div class="section-title">👥 Top Customers</div>',
    unsafe_allow_html=True
)


if "customerid" in filtered_df.columns:

    customer_data = (
        filtered_df
        .groupby("customerid", as_index=False)
        .agg(
            Orders=("orderid", "count"),
            Revenue=("totalprice", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )


    fig_customers = px.bar(
        customer_data,
        x="customerid",
        y="Revenue",
        title="Top 10 Customers by Revenue"
    )

    fig_customers.update_layout(
        xaxis_title="Customer ID",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )


# ============================================================
# TOP PRODUCTS TABLE
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Top Performing Products</div>',
    unsafe_allow_html=True
)


if "product" in filtered_df.columns:

    top_products = (
        filtered_df
        .groupby("product", as_index=False)
        .agg(
            Orders=("orderid", "count"),
            Units_Sold=("quantity", "sum"),
            Revenue=("totalprice", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    top_products["Revenue"] = (
        top_products["Revenue"]
        .round(2)
    )

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SALES DATA TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📋 Sales Data</div>',
    unsafe_allow_html=True
)


display_data = filtered_df.copy()


# ------------------------------------------------------------
# DATE DISPLAY
# ------------------------------------------------------------

if "date" in display_data.columns:

    display_data["date"] = (
        display_data["date"]
        .dt.strftime("%Y-%m-%d")
    )


# ------------------------------------------------------------
# ROUND MONEY VALUES
# ------------------------------------------------------------

if "unitprice" in display_data.columns:

    display_data["unitprice"] = (
        display_data["unitprice"]
        .round(2)
    )


if "totalprice" in display_data.columns:

    display_data["totalprice"] = (
        display_data["totalprice"]
        .round(2)
    )


# ------------------------------------------------------------
# REMOVE HELPER COLUMNS FROM DISPLAY
# ------------------------------------------------------------

helper_columns = [
    "year",
    "month",
    "year_month"
]

display_data = display_data.drop(
    columns=[
        column
        for column in helper_columns
        if column in display_data.columns
    ]
)


st.dataframe(
    display_data,
    use_container_width=True,
    height=450,
    hide_index=True
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.markdown(
    '<div class="section-title">⬇️ Download Filtered Data</div>',
    unsafe_allow_html=True
)


download_data = filtered_df.copy()


if "date" in download_data.columns:

    download_data["date"] = (
        download_data["date"]
        .dt.strftime("%Y-%m-%d")
    )


download_csv = download_data.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download CSV",
    data=download_csv,
    file_name="filtered_ecommerce_sales.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        E-Commerce Sales Data Analytics
        | Python • Pandas • SQL • Streamlit • Plotly
    </div>
    """,
    unsafe_allow_html=True
)