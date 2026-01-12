import streamlit as st
from UI_components.order_card import render_order_card
from utils.helpers import add_order

st.title("Orders")

orders = st.session_state.orders

tailors = st.session_state.tailors

tailor_lookup = {tailor.id: tailor for tailor in tailors}

@st.dialog("Enter details of new order")
def new_order():
    product_name = st.text_input("Product Name")
    client_name = st.text_input("Client Name")
    quantity_required = st.number_input("Quantity Required", min_value=1, step=1)
    if st.button("Submit"):
        add_order(product_name, client_name, quantity_required)
        st.success("Order added")
        st.rerun()

col1, col2, col3, col4 = st.columns(4)

with col4:
    if st.button(label = "+ New Order", type = "primary"):
        new_order()

status_filter = st.multiselect(
    "Filter by status",
    options=["Unassigned", "In progress", "Completed"],
    default=["Unassigned", "In progress", "Completed"],
)

filtered_orders = [
    order for order in orders
    if order.status in status_filter
]

for order in filtered_orders:
    render_order_card(order, tailor_lookup)