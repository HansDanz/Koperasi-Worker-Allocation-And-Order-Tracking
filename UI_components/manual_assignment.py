import streamlit as st

tailors = st.session_state.tailors

@st.dialog("Manual Assignment")
def assign_manual_dialog(order):
    st.subheader("Select Tailors Manually")

    available_tailors = [
        t for t in tailors
        if t.current_workload < t.max_capacity
    ]

    for tailor in available_tailors:
        with st.container(border=True):
            st.write(f"**{tailor.name}**")
            st.caption("Click to assign")

            if st.button("Select", key=f"manual_{tailor.id}"):
                st.session_state.selected_tailor = tailor
                st.session_state.assignment_mode = None
                st.rerun()
