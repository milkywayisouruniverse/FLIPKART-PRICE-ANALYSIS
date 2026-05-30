import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Flipkart Product Price Analysis",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:eeshika2023@localhost:5433/flipkart_analysis"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
query = "SELECT * FROM flipkart_products"
df = pd.read_sql(query, engine)

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------
df = df.dropna(subset=["retail_price", "discounted_price"])

df["discount_percent"] = (
    (df["retail_price"] - df["discounted_price"])
    / df["retail_price"]
) * 100

df["brand"] = df["brand"].fillna("Unknown")

# --------------------------------------------------
# EXTRACT CATEGORY
# --------------------------------------------------
df["main_category"] = (
    df["product_category_tree"]
    .astype(str)
    .str.extract(r'\["([^"]+)')
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

categories = ["All"] + sorted(
    df["main_category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

if selected_category != "All":
    df = df[df["main_category"] == selected_category]

brands = ["All"] + sorted(
    df["brand"].dropna().unique().tolist()
)

selected_brand = st.sidebar.selectbox(
    "Select Brand",
    brands
)

if selected_brand != "All":
    df = df[df["brand"] == selected_brand]

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("📊 Flipkart Product Price Analysis Dashboard")

st.markdown(
    "Interactive dashboard for product pricing, discounts, brands and category analysis."
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Products",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Average Price",
        f"₹{df['discounted_price'].mean():,.2f}"
    )

with col3:
    st.metric(
        "Average Discount",
        f"{df['discount_percent'].mean():.2f}%"
    )

with col4:
    st.metric(
        "Total Brands",
        df["brand"].nunique()
    )

st.divider()

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "Overview",
        "Brand Analysis",
        "Product Explorer"
    ]
)

# --------------------------------------------------
# OVERVIEW TAB
# --------------------------------------------------
with tab1:

    st.subheader("Top Categories")

top_cat = (
    df["main_category"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_cat.columns = ["Category", "Count"]

# Short category names
top_cat["Category"] = (
    top_cat["Category"]
    .astype(str)
    .str.split(">>")
    .str[-1]
    .str.strip()
)

fig1 = px.bar(
    top_cat,
    x="Count",
    y="Category",
    orientation="h",
    text="Count",
    title="Top 10 Categories"
)

fig1.update_layout(
    height=600,
    yaxis_title="",
    xaxis_title="Number of Products"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)
# --------------------------------------------------
# BRAND ANALYSIS TAB
# --------------------------------------------------
with tab2:

    st.subheader("Top Brands")

    top_brands = (
        df["brand"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_brands.columns = ["Brand", "Count"]

    fig4 = px.bar(
        top_brands,
        x="Brand",
        y="Count",
        title="Top 10 Brands"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# --------------------------------------------------
# PRODUCT EXPLORER TAB
# --------------------------------------------------
with tab3:

    st.subheader("Search Products")

    search_text = st.text_input(
        "Enter Product Name"
    )

    if search_text:
        search_results = df[
            df["product_name"]
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            search_results,
            use_container_width=True
        )

    st.subheader("Top Discounted Products")

    top_discount = (
        df[
            [
                "product_name",
                "brand",
                "retail_price",
                "discounted_price",
                "discount_percent"
            ]
        ]
        .sort_values(
            "discount_percent",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_discount,
        use_container_width=True
    )

# --------------------------------------------------
# DOWNLOAD BUTTON
# --------------------------------------------------
st.divider()

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="flipkart_filtered_data.csv",
    mime="text/csv"
)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------
with st.expander("View Dataset"):
    st.dataframe(
        df,
        use_container_width=True
    )