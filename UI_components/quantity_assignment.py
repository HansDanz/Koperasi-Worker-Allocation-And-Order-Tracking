import streamlit as st
from utils.helpers import commit_assignment
from models.tailor import Tailor

tailors = st.session_state.tailors

tailor_lookup = {tailor.id: tailor for tailor in tailors}

@st.dialog("Enter quota for each tailor")
def assign_quantity_dialog(order):

    st.subheader(f"Order: {order.product_name}")
    st.caption(f"Total required: {order.quantity_required}")

    total_assigned = 0

    for tailor_id in st.session_state.selected_tailors:
        tailor = tailor_lookup[tailor_id]

        # Initialize default if missing
        if tailor_id not in st.session_state.quantity_allocation:
            st.session_state.quantity_allocation[tailor_id] = 0

        qty = st.number_input(
            label=f"{tailor.name}",
            min_value=0,
            max_value=order.quantity_required,
            step=1,
            key=f"qty_{tailor_id}",
            value=st.session_state.quantity_allocation[tailor_id]
        )

        st.session_state.quantity_allocation[tailor_id] = qty
        total_assigned += qty
    
    st.divider()

    if total_assigned < order.quantity_required:
        st.warning(
            f"{order.quantity_required - total_assigned} pieces unassigned"
        )
    elif total_assigned > order.quantity_required:
        st.error(
            f"{total_assigned - order.quantity_required} pieces over-allocated"
        )
    else:
        st.success("Quantity allocation is valid ✅")

    col1, col2 = st.columns(2)

    with col1:
        if (
            total_assigned == order.quantity_required
            and st.button("Accept Allocation")
        ):
            order.tailors_involved = dict(st.session_state.quantity_allocation)

            # Cleanup
            st.session_state.quantity_allocation.clear()
            st.session_state.selected_tailors.clear()
            st.session_state.assignment_mode = None

            st.rerun()

    with col2:
        if st.button("Reject & Reassign"):
            st.session_state.quantity_allocation.clear()
            st.session_state.assignment_mode = "MANUAL"
            st.rerun()



            
