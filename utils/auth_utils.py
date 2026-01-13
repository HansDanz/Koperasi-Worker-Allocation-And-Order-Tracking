import streamlit as st
import time


def check_auth():
    """
    Checks if the user is logged in. If not, redirects to the Login page.
    Should be called at the very top of every protected page.
    """
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # Redirect immediately
        st.switch_page("pages/0_Login.py")
        st.stop()

    # Always hide the "Login" page from sidebar if possible, to keep it clean
    inject_global_styles()
    
    # Ensure Logout button is present on all protected pages
    logout_button()

def logout_button():
    """
    Adds a logout button to the sidebar.
    """
    with st.sidebar:
        st.divider() # Separator
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

def inject_global_styles():
    """
    Injects global CSS for:
    1. Hiding strict login page from sidebar.
    2. Forcing Primary buttons to be Blue (#3b82f6).
    """
    st.markdown(
        """
        <style>
            /* Hide the entry for 0_Login.py in the sidebar nav */
            [data-testid="stSidebarNav"] li:has(a[href$="Login"]) {
                display: none;
            }
            
            /* GLOBAL: Force Primary (Action) Buttons to be Blue */
            div.stButton > button[kind="primary"] {
                background-color: #3b82f6 !important;
                border-color: #3b82f6 !important;
                color: white !important;
            }
            div.stButton > button[kind="primary"]:hover {
                background-color: #2563eb !important;
                border-color: #2563eb !important;
            }
            div.stButton > button[kind="primary"]:focus {
                color: white !important;
            }
            /* Sidebar Logout Button: Red */
            [data-testid="stSidebar"] button[kind="secondary"] {
                color: #ef4444 !important;
                border-color: #ef4444 !important;
            }
            [data-testid="stSidebar"] button[kind="secondary"]:hover {
                color: #dc2626 !important;
                border-color: #dc2626 !important;
                background-color: #fef2f2 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def hide_sidebar():
    """
    Hides the sidebar completely (useful for Login page).
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
