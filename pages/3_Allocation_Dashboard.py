import streamlit as st
from UI_components.order_card import render_order_card
from UI_components.tailor_card import render_tailor_card
from UI_components.ml_assignment import assign_ml_dialog
from UI_components.manual_assignment import assign_manual_dialog

orders = st.session_state.orders

tailors = st.session_state.tailors

tailor_lookup = {tailor.id: tailor for tailor in tailors}

st.title("Allocation Dashboard")

unassigned_orders = [order for order in orders if order.status == "Unassigned"]

if not unassigned_orders:
    st.info("All orders have been assigned 🎉")

for order in unassigned_orders:
    render_order_card(order, tailor_lookup)

if st.session_state.assignment_mode == "ML":
    st.session_state.assignment_mode = None
    assign_ml_dialog(st.session_state.current_order)

elif st.session_state.assignment_mode == "MANUAL":
    st.session_state.assignment_mode = None
    assign_manual_dialog(st.session_state.current_order)







