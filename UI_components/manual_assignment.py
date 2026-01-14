import streamlit as st

tailors = st.session_state.tailors

@st.dialog("Manual Assignment")
def assign_manual_dialog(order):
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Select Tailors Manually")
        
        # Inject Blue CSS for Dialog
        st.markdown("""
            <style>
            div.stButton > button[kind="primary"] {
                background-color: #3b82f6 !important;
                border-color: #3b82f6 !important;
                color: white !important;
            }
            div.stButton > button[kind="primary"]:hover {
                background-color: #2563eb !important;
                border-color: #2563eb !important;
            }
            </style>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Submit", type="primary", use_container_width=True):
            st.session_state.assignment_mode = "QTY"
            st.rerun()

    orders = st.session_state.orders
    
    # SOP: One Order Per Tailor
    busy_tailor_ids = set()
    for o in orders:
        if o.status != "COMPLETED" and o.tailors_involved:
            for tid in o.tailors_involved:
                busy_tailor_ids.add(tid)

    available_tailors = [
        t for t in tailors
        if t.current_workload < t.max_capacity and t.id not in busy_tailor_ids
    ]
    
    busy_list = [t for t in tailors if t.id in busy_tailor_ids]

    # --- Available Tailors ---
    for tailor in available_tailors:
        with st.expander(f"{tailor.name}", expanded=False):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write("**Skills**")
                for skill, level in tailor.skill_vector.items():
                    if isinstance(level, (int, float)):
                        # Skills are 1-10, progress expects 0.0-1.0
                        normalized_level = min(max(level / 10.0, 0.0), 1.0)
                        st.progress(normalized_level, text=f"{skill} ({level})")
                    else:
                        st.write(f"**{skill.capitalize()}:** {level}")

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

    # --- Busy Tailors Section ---
    if busy_list:
        st.divider()
        st.caption("⛔ Unavailable (Currently assigned to an active order)")
        for tailor in busy_list:
             # Find which order they are on? (Optional, but nice info)
             active_order_id = next((o.id for o in orders if o.status != "COMPLETED" and tailor.id in (o.tailors_involved or [])), "Unknown")
             
             with st.container(border=True):
                 b_col1, b_col2 = st.columns([3, 1])
                 with b_col1:
                     st.write(f"**{tailor.name}**")
                     st.caption(f"Busy on Order #{active_order_id}")
                 with b_col2:
                     st.button("Busy", key=f"busy_{tailor.id}", disabled=True)


