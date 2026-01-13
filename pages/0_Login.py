
import streamlit as st
import time
from utils.auth_utils import hide_sidebar

st.set_page_config(layout="wide", page_title="Login")
hide_sidebar()

st.title("Login to Allocation System")

# Simple check
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.success("You are already logged in.")
    # Auto-redirect if already logged in
    time.sleep(0.5)
    st.switch_page("Instructions.py")
else:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Login successful!")
            time.sleep(0.5)
            st.switch_page("Instructions.py")
        else:
            st.error("Invalid username or password")

st.info("Default credentials: admin / admin")
