import streamlit as st
import pandas as pd

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# (1) Add a drop-down for Category
selected_category = st.selectbox("Select a Category", df['Category'].unique())

# Filter dataframe based on selected category
filtered_df = df[df['Category'] == selected_category]

# (2) Add a multi-select for Sub-Category in the selected Category
selected_subcategories = st.multiselect(
    "Select Sub_Category", 
    filtered_df['Sub_Category'].unique()
)

# Filter dataframe further based on selected sub-categories
if selected_subcategories:
    filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]

# (3) Show a line chart of sales for the selected items
if not filtered_df.empty:
    filtered_df["Order_Date"] = pd.to_datetime(filtered_df["Order_Date"])
    filtered_df.set_index('Order_Date', inplace=True)
    
    # Aggregate sales by month
    sales_by_month = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    
    st.write("### Sales Over Time")
    st.line_chart(sales_by_month, y="Sales")

# (4) Show three metrics: total sales, total profit, and overall profit margin (%)
if not filtered_df.empty:
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    
    # Calculate overall profit margin for comparison (all products across all categories)
    total_sales_all = df['Sales'].sum()
    total_profit_all = df['Profit'].sum()
    overall_avg_profit_margin = (total_profit_all / total_sales_all) * 100 if total_sales_all != 0 else 0
    
    # Calculate the delta between selected items' profit margin and overall profit margin
    profit_margin_delta = overall_profit_margin - overall_avg_profit_margin
    
    # Display metrics
    st.write("### Metrics for Selected Sub_Categories")
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Overall Profit Margin (%)", f"{overall_profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")


