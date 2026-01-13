import streamlit as st
import time


def check_auth():
    """
    Checks if the user is logged in. If not, redirects to the Login page.
    Should be called at the very top of every protected page.
    """
    # Always hide the "Login" page from sidebar if possible, to keep it clean
    add_sidebar_styling()

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        # Redirect immediately
        st.switch_page("pages/0_Login.py")
        st.stop()

def logout_button():
    """
    Adds a logout button to the sidebar.
    """
    with st.sidebar:
        st.divider() # Separator
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

def add_sidebar_styling():
    """
    Injects CSS to hide the 'Login' page from the sidebar navigation.
    """
    st.markdown(
        """
        <style>
            /* Hide the entry for 0_Login.py in the sidebar nav */
            [data-testid="stSidebarNav"] li:has(a[href$="Login"]) {
                display: none;
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
