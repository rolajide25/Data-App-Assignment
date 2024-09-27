import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])
st.dataframe(df)

# Dropdown for selecting Category
selected_category = st.selectbox("Select a Category", df['Category'].unique())

# Multi-select for Sub-Category based on the selected Category
filtered_df = df[df['Category'] == selected_category]
selected_subcategories = st.multiselect("Select Sub-Category", filtered_df['Sub_Category'].unique())

# Filter the dataframe by selected sub-categories
filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]

# Sort by Order_Date to ensure the line chart is in ascending order by date
filtered_df = filtered_df.sort_values(by='Order_Date')

# Create a line chart for Sales with different colors for each Sub-Category
if not filtered_df.empty:
    plt.figure(figsize=(10, 6))
    
    for subcategory in selected_subcategories:
        subcategory_data = filtered_df[filtered_df['Sub_Category'] == subcategory]
        # Group by date to aggregate sales
        sales_by_date = subcategory_data.groupby('Order_Date')['Sales'].sum()
        plt.plot(sales_by_date.index, sales_by_date.values, label=subcategory)

    plt.title('Sales by Sub-Category')
    plt.xlabel('Order Date')
    plt.ylabel('Sales')
    plt.legend(title='Sub-Category')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Set Y-axis ticks for better clarity
    max_sales = int(filtered_df['Sales'].max())
    y_ticks = range(0, max_sales + 10000, 10000)  # Adjust step size as needed
    plt.yticks(y_ticks)

    # Show the plot in Streamlit
    st.pyplot(plt)

    # Calculate metrics for selected items
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # Display metrics
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")
else:
    st.write("Please select at least one Sub_Category to view the sales data.")
