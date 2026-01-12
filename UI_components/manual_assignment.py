import streamlit as st

tailors = st.session_state.tailors

@st.dialog("Manual Assignment")
def assign_manual_dialog(order):
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Select Tailors Manually")
    
    with col2:
        if st.button("Submit"):
            st.session_state.assignment_mode = "QTY"
            st.rerun()

    available_tailors = [
        t for t in tailors
        if t.current_workload < t.max_capacity
    ]

    for tailor in available_tailors:
        with st.expander(f"{tailor.name}", expanded=False):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write("**Skills**")
                for skill, level in tailor.skill_vector.items():
                    st.progress(level, text=skill)

                st.write(f"Reliability: {tailor.reliability_score}")
                st.write(
                    f"Workload: {tailor.current_workload}/{tailor.max_capacity}"
                )
                st.write(f"Availability: {tailor.availability_hours} hrs")

            with col2:
                selected = tailor.id in st.session_state.selected_tailors

                if st.button(
                    "Remove" if selected else "Select",
                    key=f"select_{tailor.id}"
                ):
                    if selected:
                        st.session_state.selected_tailors.remove(tailor.id)
                    else:
                        st.session_state.selected_tailors.add(tailor.id)
                    st.rerun()


