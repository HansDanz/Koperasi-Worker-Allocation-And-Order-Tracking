import streamlit as st
from utils.helpers import commit_assignment

def render_manual_quantity_assignment(order):
    st.subheader("Recommended Tailors")

    allocation = {}

    '''
    for tailor, score in st.session_state.ml_suggestion:
        with st.container(border=True):
            st.write(f"**{tailor.name}**")
            st.caption(f"Match score: {score:.2f}")

            allocation[tailor.id] = st.number_input(
                "Assign quantity",
                min_value=0,
                max_value=tailor.max_capacity - tailor.current_workload,
                key=f"ml_qty_{tailor.id}"
            )
    '''
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Accept"):
            commit_assignment(order, allocation)
            st.rerun()

    with col2:
        if st.button("Reject & Choose Manually"):
            st.session_state.assignment_mode = "MANUAL"
            st.rerun()

            
