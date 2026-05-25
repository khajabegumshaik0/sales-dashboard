import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# Title
st.title("📊 Sales & Revenue Analysis Dashboard")

# Upload File
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read CSV or Excel
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Convert Date
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    # Sidebar Filters
    st.sidebar.header("Filters")

    selected_region = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    selected_category = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    # Filter Data
    filtered_df = df[
        (df["Region"].isin(selected_region)) &
        (df["Category"].isin(selected_category))
    ]

    # KPI Calculations
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["OrderID"].nunique()

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"₹ {total_sales:,.2f}")
    col2.metric("📈 Total Profit", f"₹ {total_profit:,.2f}")
    col3.metric("🛒 Total Orders", total_orders)

    st.markdown("---")

    # Sales Trend
    st.subheader("📅 Sales Trend")

    sales_trend = filtered_df.groupby("OrderDate")["Sales"].sum().reset_index()

    fig1 = px.line(
        sales_trend,
        x="OrderDate",
        y="Sales",
        markers=True,
        title="Revenue Over Time"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Top Products
    st.subheader("🏆 Top Products")

    top_products = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_products,
        x="Product",
        y="Sales",
        color="Sales",
        title="Top 10 Products"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Region Sales
    st.subheader("🌍 Region Wise Sales")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales Distribution by Region"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Full Data
    st.subheader("📋 Dataset")

    st.dataframe(filtered_df)

else:
    st.info("Please upload a CSV or Excel file.")