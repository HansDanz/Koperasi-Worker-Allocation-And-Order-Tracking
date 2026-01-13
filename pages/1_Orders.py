import streamlit as st
from utils.auth_utils import check_auth

check_auth()

from UI_components.order_card import render_order_card
from utils.helpers import add_order
from UI_components.ml_assignment import assign_ml_dialog
from UI_components.manual_assignment import assign_manual_dialog
from UI_components.quantity_assignment import assign_quantity_dialog
from models.order import Order
from UI_components.order_detail_view import render_order_detail

st.title("Orders Management")

orders = st.session_state.orders
tailors = st.session_state.tailors
tailor_lookup = {tailor.id: tailor for tailor in tailors}

# --- Action Handler (Query Params) ---
# Removed as we reverted to native buttons to fix SecurityError
# -------------------------------------

# Dialog for new order
@st.dialog("Enter details of new order")
def new_order():
    product_name = st.selectbox("Product Name", ["School Uniform", "Batik Shirt", "Sports Jersey"], index=None, placeholder="Select or type...", accept_new_options=True)
    client_name = st.text_input("Client Name")
    quantity_required = st.number_input("Quantity Required", min_value=1, step=1)
    deadline = st.date_input("Deadline")
    
    if st.button("Submit"):
        # Create order properly
        # Note: add_order util usually takes partial args, might need updating or direct append
        # For compatibility, we'll use the helper if it matches, else manual append
        add_order(product_name, client_name, quantity_required) 
        # Since add_order might not set deadline, we might want to update the last added order
        # But for now let's rely on defaults or update helper later
        st.success("Order added")
        st.rerun()

col1, col2 = st.columns([3, 1])
with col2:
    if st.button(label = "+ New Order", type = "primary", use_container_width=True):
        new_order()


# Filter & Sort Options
col_filter, col_sort = st.columns([2, 1])

with col_filter:
    filter_option = st.selectbox(
        "View Orders",
        ["All", "Pre-Production", "In Production", "Finished"],
        index=0
    )

# Logic for categorizing statuses
status_map = {
    "Pre-Production": ["DRAFT", "PROOFING", "MATERIAL_SOURCING"],
    "In Production": ["CUTTING", "SEWING"],
    "Finished": ["DISTRIBUTION", "COMPLETED"] # Distribution is now delivery to customer
}

from UI_components.order_detail_view import render_order_detail

# ... (imports)

# 1. Filter
if filter_option == "All":
    filtered_orders = orders
else:
    allowed_statuses = status_map.get(filter_option, [])
    filtered_orders = [o for o in orders if o.status in allowed_statuses]

# 2. Sort by Deadline (Urgency), then by Assignment Status (Unassigned first)
filtered_orders.sort(key=lambda x: (
    x.deadline_date if x.deadline_date else "9999-12-31", 
    bool(x.tailors_involved) # False (0) < True (1), so Unassigned shows first
))

# Display Logic: Detail View vs List View
if "detail_order_id" in st.session_state and st.session_state.detail_order_id is not None:
    # Find the order
    order_detail = next((o for o in orders if o.id == st.session_state.detail_order_id), None)
    if order_detail:
        render_order_detail(order_detail, tailor_lookup)
    else:
        st.error("Order not found.")
        if st.button("Back to List"):
            st.session_state.detail_order_id = None
            st.rerun()
else:
    # List View
    if not filtered_orders:
        st.info(f"No orders found in '{filter_option}'")
    else:
        for order in filtered_orders:
            render_order_card(order, tailor_lookup)

# Assignment Dialogs Logic
# Only open dialogs if they were triggered from this page
if st.session_state.get("assignment_origin") == "Orders":
    if st.session_state.assignment_mode == "ML":
        st.session_state.assignment_mode = None
        assign_ml_dialog(st.session_state.current_order)

    elif st.session_state.assignment_mode == "MANUAL":
        st.session_state.assignment_mode = None
        assign_manual_dialog(st.session_state.current_order)

    elif st.session_state.assignment_mode == "QTY":
        st.session_state.assignment_mode = None
        assign_quantity_dialog(st.session_state.current_order)