import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

sns.set_style("whitegrid")

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        Path(__file__).parent / "main_data.csv"
    )

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce"
    )

    return df

all_df = load_data()

# ==================================================
# DATA PREPARATION
# ==================================================

all_df["item_revenue"] = (
    all_df["price"] +
    all_df["freight_value"]
)

# Data unik untuk revenue/payment
revenue_base = (
    all_df[
        [
            "order_id",
            "order_purchase_timestamp",
            "payment_sequential",
            "payment_type",
            "payment_value"
        ]
    ]
    .drop_duplicates()
)

# ==================================================
# HEADER
# ==================================================

st.title("🛒 E-Commerce Public Dataset Dashboard")

st.markdown("""
Dashboard analisis E-Commerce Public Dataset.
""")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Dashboard Information")

st.sidebar.write("""
**Proyek Analisis Data**

Nama: Tarwin

Dataset: E-Commerce Public Dataset
""")


st.sidebar.header("Filter")

# Tahun
available_years = sorted(
    all_df["order_purchase_timestamp"]
    .dt.year
    .dropna()
    .unique()
)

year_options = ["Semua Tahun"] + [
    str(year) for year in available_years
]

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    year_options
)

# Bulan
month_options = [
    "Semua Bulan",
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember"
]

selected_month = st.sidebar.selectbox(
    "Pilih Bulan",
    month_options
)

# Filter awal
filtered_df = all_df.copy()
filtered_revenue = revenue_base.copy()

# Filter tahun
if selected_year != "Semua Tahun":
    selected_year = int(selected_year)

    filtered_df = filtered_df[
        filtered_df["order_purchase_timestamp"].dt.year
        == selected_year
    ]

    filtered_revenue = filtered_revenue[
        filtered_revenue["order_purchase_timestamp"].dt.year
        == selected_year
    ]

# Filter bulan
if selected_month != "Semua Bulan":

    month_number = month_options.index(selected_month)

    filtered_df = filtered_df[
        filtered_df["order_purchase_timestamp"].dt.month
        == month_number
    ]

    filtered_revenue = filtered_revenue[
        filtered_revenue["order_purchase_timestamp"].dt.month
        == month_number
    ]
# ==================================================
# METRICS
# ==================================================

total_revenue = filtered_revenue["payment_value"].sum()

total_orders = filtered_revenue["order_id"].nunique()

total_customers = filtered_df["customer_unique_id"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"R$ {total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

# ==================================================
# MONTHLY REVENUE
# ==================================================

monthly_df = filtered_revenue.copy()

monthly_df["year_month"] = (
    monthly_df["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

monthly_revenue = (
    monthly_df
    .groupby("year_month")["payment_value"]
    .sum()
    .reset_index()
)

st.subheader("📈 Monthly Revenue Trend")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    monthly_revenue["year_month"],
    monthly_revenue["payment_value"],
    marker="o"
)

ax.set_title("Monthly Revenue Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue")

plt.xticks(rotation=45)

st.pyplot(fig)

# ==================================================
# TOP PRODUCT CATEGORY
# ==================================================

category_revenue = (
    filtered_df
    .groupby("product_category_name_english")["item_revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_10_categories = (
    category_revenue
    .head(10)
    .reset_index()
)

st.subheader("🏆 Top 10 Product Categories by Revenue")

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=top_10_categories,
    x="item_revenue",
    y="product_category_name_english",
    ax=ax
)

ax.set_title("Top 10 Product Categories by Revenue")
ax.set_xlabel("Revenue")
ax.set_ylabel("Product Category")

st.pyplot(fig)

# ==================================================
# PAYMENT TYPE
# ==================================================

payment_average = (
    filtered_revenue
    .groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

st.subheader("💳 Average Transaction Value by Payment Type")

fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=payment_average,
    x="payment_type",
    y="payment_value",
    ax=ax
)

ax.set_title("Average Transaction Value by Payment Type")
ax.set_xlabel("Payment Type")
ax.set_ylabel("Average Transaction Value")

st.pyplot(fig)

# ==================================================
# REVIEW DISTRIBUTION
# ==================================================

if "review_score" in filtered_df.columns:

    st.subheader("⭐ Review Score Distribution")

    review_dist = (
        filtered_df["review_score"]
        .dropna()
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x=review_dist.index,
        y=review_dist.values,
        ax=ax
    )

    ax.set_title("Review Score Distribution")
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Total Reviews")

    st.pyplot(fig)

# ==================================================
# TOP SELLER STATES
# ==================================================

if "seller_state" in filtered_df.columns:

    seller_state = (
        filtered_df["seller_state"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    seller_state.columns = [
        "seller_state",
        "total_sellers"
    ]

    st.subheader("🏪 Top 10 Seller States")

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=seller_state,
        x="seller_state",
        y="total_sellers",
        ax=ax
    )

    ax.set_title("Top 10 Seller States")
    ax.set_xlabel("State")
    ax.set_ylabel("Total Sellers")

    st.pyplot(fig)

# ==================================================
# INSIGHT
# ==================================================

st.subheader("📌 Key Insights")

st.markdown("""
1. Revenue meningkat sepanjang 2017 dan mencapai puncak pada November 2017.

2. Kategori health_beauty, watches_gifts, dan bed_bath_table memberikan kontribusi revenue terbesar.

3. Credit card memiliki rata-rata nilai transaksi tertinggi.

4. Mayoritas pelanggan memberikan review score 5.

5. Sebagian besar seller berasal dari SP (São Paulo).
""")
