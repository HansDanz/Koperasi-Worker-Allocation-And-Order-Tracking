import streamlit as st

st.write(st.session_state)

for order in st.session_state.orders:
    st.write(order.placement_date, order.due_date)