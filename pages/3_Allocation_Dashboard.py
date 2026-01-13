import streamlit as st
from utils.auth_utils import check_auth

check_auth()

from models.order import Order
from UI_components.ml_assignment import assign_ml_dialog
from UI_components.manual_assignment import assign_manual_dialog
from UI_components.quantity_assignment import assign_quantity_dialog

st.title("Allocation Dashboard")
st.caption("Focused view for assigning workers to orders. SOP enforced: Workers can only handle one active order.")

orders = st.session_state.orders
tailors = st.session_state.tailors

# Filter: Orders in SEWING status that have NO tailors assigned yet
# This defines the "Queue" for the allocation manager
pending_assignment = [
    o for o in orders 
    if o.status == "SEWING" and not o.tailors_involved
]

if not pending_assignment:
    st.success("🎉 All active sewing orders have tailors assigned! No pending allocations.")
    # Optional: Show upcoming orders (Cutting)
    upcoming = [o for o in orders if o.status == "CUTTING"]
    if upcoming:
        st.info(f"{len(upcoming)} orders are currently in CUTTING phase and will need assignment soon.")
else:
    for order in pending_assignment:
        # Specialized Card for Allocation
        with st.container(border=True):
            col_info, col_action = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"### {order.product_name}")
                st.caption(f"Client: {order.client_name} | ID: {order.id}")
                st.write(f"**Deadline:** {order.deadline_date}")
                st.write(f"**Quantity Required:** {order.quantity_required} pcs")
                
            with col_action:
                st.write("") # Spacer
                if st.button("Assign Workers", key=f"dash_assign_{order.id}", type="primary", use_container_width=True):
                    st.session_state.current_order = order
                    st.session_state.assignment_mode = "ML" 
                    st.session_state.assignment_origin = "Allocation"
                    st.rerun()

# --- Dialog Handling ---
# Only open dialogs if they were triggered from this page
if st.session_state.get("assignment_origin") == "Allocation":
    if st.session_state.assignment_mode == "ML":
        st.session_state.assignment_mode = None
        assign_ml_dialog(st.session_state.current_order)

    elif st.session_state.assignment_mode == "MANUAL":
        st.session_state.assignment_mode = None
        assign_manual_dialog(st.session_state.current_order)

    elif st.session_state.assignment_mode == "QTY":
        st.session_state.assignment_mode = None
        assign_quantity_dialog(st.session_state.current_order)







