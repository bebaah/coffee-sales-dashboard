import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu 


st.set_page_config(layout="wide")

def load_data(file_path):
    data=pd.read_csv(file_path)
    return data

data=pd.read_csv("coffeeshopsales.csv")

st.title("Coffee Shop Sales Dashboard")

# -------- Navbar -------- #
select = option_menu(
    menu_title=None,
    options=["Home","Sales Analysis","Store Insights","Product Comparison","Data Explorer"],
    orientation="horizontal"  
)

# -------- Sidebar Filters -------- #
st.sidebar.header("Filters")

store=st.sidebar.multiselect(
    "Select Store",
    options=data["store_location"].unique()
)

product=st.sidebar.multiselect(
    "Select Product",
    options=data["product_type"].unique()
)

size=st.sidebar.multiselect(
    "Select Size",
    options=data["Size"].unique()
)

filtered_data=data.copy()

if store:
    filtered_data = filtered_data[filtered_data["store_location"].isin(store)]
if product:
    filtered_data = filtered_data[filtered_data["product_type"].isin(product)]
if size:
    filtered_data = filtered_data[filtered_data["Size"].isin(size)]

# -------- Home -------- #
if select == "Home":
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", filtered_data["transaction_id"].nunique())
    col2.metric("Total Revenue", int(filtered_data["Total_bill"].sum()))
    col3.metric("Total Products", filtered_data["product_type"].nunique())

    st.dataframe(filtered_data)

# -------- Sales Analysis -------- #
elif select == "Sales Analysis":
    st.subheader("Sales Analysis")

    sales_by_date = filtered_data.groupby("transaction_date")["Total_bill"].sum().reset_index()

    fig = px.line(
        sales_by_date,
        x="transaction_date",
        y="Total_bill",
        title="Sales Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------- Store Insights -------- #
elif select=="Store Insights":
    st.subheader("Store Insights")

    store_sales=filtered_data.groupby("store_location")["Total_bill"].sum().reset_index()

    fig=px.pie(
        store_sales,
        names="store_location",
        values="Total_bill",
        title="Sales by Store"
    )

    st.plotly_chart(fig, use_container_width=True)





# -------- Product Comparison -------- #
elif select=="Product Comparison":
    st.subheader("Product Comparison")

    fig=px.bar(
        filtered_data,
        x="product_type",
        y="Total_bill",
        color="Size",
        title="Product Sales Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)




# -------- Data Explorer -------- #
elif select=="Data Explorer":
    st.subheader("Data Explorer")
    st.dataframe(filtered_data)