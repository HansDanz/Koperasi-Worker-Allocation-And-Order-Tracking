import streamlit as st
from data.dummy_data import get_dummy_orders, get_dummy_tailors

if "orders" not in st.session_state:
    st.session_state.orders = get_dummy_orders()

if "tailors" not in st.session_state:
    st.session_state.tailors = get_dummy_tailors()

if  "assignment_mode" not in st.session_state:
    st.session_state.assignment_mode = None  # or "MANUAL"

if  "current_order" not in st.session_state:
    st.session_state.current_order = None

if "ml_suggestion" not in st.session_state:
    st.session_state.ml_suggestion = {}

if "manual_selected_tailors" not in st.session_state:
    st.session_state.selected_tailors = set()

if "quantity_allocation" not in st.session_state:
    st.session_state.quantity_allocation = {}