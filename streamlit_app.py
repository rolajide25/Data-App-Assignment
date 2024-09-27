import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])
st.dataframe(df)

# Display bar charts for category sales
st.write("### Sales by Category")
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Set Order_Date as the index for time-based aggregation
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

# Monthly sales aggregation
sales_by_month = df.resample('M')['Sales'].sum()
st.write("### Monthly Sales Data")
st.dataframe(sales_by_month)

# Line chart for monthly sales
st.line_chart(sales_by_month)

# Adding dropdown for Category
selected_category = st.selectbox("Select a Category", df['Category'].unique())

# Filtering data based on the selected Category
filtered_df = df[df['Category'] == selected_category]

# Adding multi-select for Sub-Category
selected_subcategories = st.multiselect("Select Sub-Category", filtered_df['Sub_Category'].unique())

# Filter the dataframe by selected sub-categories
if selected_subcategories:
    filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]
    
    # Line chart for selected sub-categories
    plt.figure(figsize=(12, 6))
    
    for subcategory in selected_subcategories:
        subcategory_data = filtered_df[filtered_df['Sub_Category'] == subcategory]
        sales_by_date = subcategory_data.resample('M')['Sales'].sum()
        plt.plot(sales_by_date.index, sales_by_date.values, label=subcategory, marker='o')

    plt.title('Sales by Sub-Category', fontsize=16)
    plt.xlabel('Order Date', fontsize=14)
    plt.ylabel('Sales ($)', fontsize=14)
    plt.legend(title='Sub-Category', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    # Show the plot in Streamlit
    st.pyplot(plt)

    # Calculate metrics for selected items
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    
    # Overall average profit margin
    overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100 if df['Sales'].sum() > 0 else 0

    # Display metrics
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=profit_margin - overall_avg_profit_margin)
else:
    st.write("Please select at least one Sub_Category to view the sales data.")
