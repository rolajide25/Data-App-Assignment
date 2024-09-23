import streamlit as st
import pandas as pd

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Bar chart without aggregation
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Time-based aggregation
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# Additions as per your requirements
st.write("## Your Additions")

# (1) Dropdown for Category selection
category = st.selectbox("Select Category", df['Category'].unique())

# (2) Multi-select for Sub_Category based on selected Category
sub_category_options = df[df['Category'] == category]['Sub_Category'].unique()
sub_categories = st.multiselect("Select Sub_Category", sub_category_options)

# Filter data based on selections
filtered_data = df[(df['Category'] == category) & (df['Sub_Category'].isin(sub_categories))]

# (3) Line chart for selected items in (2)
if not filtered_data.empty:
    # Grouping the filtered data by month and summing sales
    sales_by_month_filtered = filtered_data.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

    # Display the line chart of sales for the selected items
    st.line_chart(sales_by_month_filtered, y="Sales")

    # (4) Metrics: total sales, total profit, and overall profit margin for the selected items
    total_sales = filtered_data['Sales'].sum()
    total_profit = filtered_data['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # Calculate the overall average profit margin
    overall_sales = df['Sales'].sum()
    overall_profit = df['Profit'].sum()
    overall_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales > 0 else 0

    # (5) Metrics display with delta for profit margin
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{profit_margin - overall_profit_margin:.2f}%")
else:
    st.write("Please select at least one Sub_Category to see the results.")
