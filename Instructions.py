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

<<<<<<< Updated upstream
=======
# --- User Instructions ---

st.markdown("""
### Manager's Guide
This application helps you manage production orders, allocate tailors, and track financial performance. Here is how to use it:

#### 1. Manage Orders (`Orders` Page)
*   **View Orders**: See all incoming and ongoing projects sorted by most recent first.
*   **Track Status**: Check if a project is in "DRAFT", "SEWING", or "COMPLETED".
*   **Search & Filter**: Use the sidebar tool to find specific orders (e.g., "Jerseys") or filter by status (e.g., "In Production").

#### 2. Allocate Workers (`Allocation Dashboard`)
*   **AI Recommendations**: Select a new order to see intelligent tailor recommendations based on **Specialty** (Uniform vs Custom) and **Availability**.
*   **Assign Work**: 
    *   Click "Manual Assign" to pick specific workers.
    *   Distribute the quantity (e.g., Order of 100 items -> 50 to Tailor A, 50 to Tailor B).
    *   Once confirmed, the system updates the tailor's status.

#### 3. Monitor Workforce (`Tailors` Page)
*   **Worker Profiles**: View detailed profiles for each tailor, including their:
    *   **Current Status**: (e.g., "Busy", "Free").
    *   **Specialty**: (e.g., "Uniforms", "All").
    *   **Performance History**: Recent jobs they have completed.

#### 4. Financial Reports (`Payroll` Page)
*   **Monthly Overview**: Check **Revenue**, **Expenses**, and **Net Profit** for any given month.
*   **Strategic Insights**: View Year-to-Date revenue trends and see which product categories (e.g., "Uniforms") are most profitable.
*   **Payroll**: Automatically calculate wages due for each tailor based on their completed work.
""")

st.info("💡 **Tip**: Navigation menu is on the left. Start by checking the **Orders** page!")

>>>>>>> Stashed changes
