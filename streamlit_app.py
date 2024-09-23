import streamlit as st
import pandas as pd

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])
st.dataframe(df)


# (1) Dropdown for Category selection
category = st.selectbox("Select Category", df['Category'].unique())

# (2) Multi-select for Sub_Category based on selected Category
sub_category_options = df[df['Category'] == category]['Sub_Category'].unique()
sub_categories = st.multiselect("Select Sub_Category", sub_category_options)

# Filter data based on selections
filtered_data = df[(df['Category'] == category) & (df['Sub_Category'].isin(sub_categories))]

# (3) Show a line chart of sales for the selected items in Sub_Category
if not filtered_data.empty:
    sales_by_month_filtered = filtered_data['Sales'].resample('M').sum()
    st.line_chart(sales_by_month_filtered)

    # (4) Show three metrics for the selected items in Sub_Category
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
