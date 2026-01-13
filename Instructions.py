import streamlit as st
from utils.auth_utils import check_auth, logout_button

st.set_page_config(layout="wide")
check_auth()  # Basic auth check - Redirects fast if not logged in

from data.dummy_data import get_dummy_orders, get_dummy_tailors
from utils.style_utils import render_tailwind

# Demo of Tailwind Integration
render_tailwind("""
    <div class="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-4" role="alert">
        <p class="font-bold">Tailwind Activated</p>
        <p>If you see this styled box (blue background), Tailwind CSS is working correctly inside this component!</p>
    </div>
""", height=150)
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

