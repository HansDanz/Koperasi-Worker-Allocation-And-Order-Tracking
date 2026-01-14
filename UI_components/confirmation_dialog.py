import streamlit as st

@st.dialog("Confirm Status Update")
def confirm_advance_dialog(order, target_stage):
    st.write(f"Are you sure you want to advance this order to **{target_stage}**?")
    st.warning("This action marks the current phase as complete.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Proceed", type="primary", key=f"confirm_yes_{order.id}"):
            if order.advance_status():
                st.rerun()
                
    with col2:
        if st.button("Cancel", key=f"confirm_no_{order.id}"):
            st.rerun()
