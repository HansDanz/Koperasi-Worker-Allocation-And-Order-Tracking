import streamlit as st
from UI_components.order_card import render_order_card
from utils.helpers import add_order
from UI_components.ml_assignment import assign_ml_dialog
from UI_components.manual_assignment import assign_manual_dialog

from UI_components.quantity_assignment import assign_quantity_dialog
from utils.auth_utils import check_auth

check_auth()

st.title("Orders")

orders = st.session_state.orders

tailors = st.session_state.tailors

tailor_lookup = {tailor.id: tailor for tailor in tailors}

@st.dialog("Enter details of new order")
def new_order():
    product_name = st.selectbox("Product Name", ["School Uniform"], index=None, placeholder="Select a product or enter a new one", accept_new_options=True)
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

status_filter = st.selectbox(
    "Filter by Order Status",
    ("Unassigned", "In progress", "Completed"),
    placeholder="Click here to filter by order type...",
    accept_new_options=False
)

filtered_orders = [
    order for order in orders
    if order.status in status_filter
]

for order in filtered_orders:
    render_order_card(order, tailor_lookup)

if st.session_state.assignment_mode == "ML":
    st.session_state.assignment_mode = None
    assign_ml_dialog(st.session_state.current_order)

elif st.session_state.assignment_mode == "MANUAL":
    assign_manual_dialog(st.session_state.current_order)

elif st.session_state.assignment_mode == "QTY":
    assign_quantity_dialog(st.session_state.current_order)