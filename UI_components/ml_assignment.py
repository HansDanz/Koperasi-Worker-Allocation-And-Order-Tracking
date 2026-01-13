import streamlit as st
from utils.helpers import commit_assignment

@st.dialog("Suggested Assignment")
def assign_ml_dialog(order):
    st.subheader("Recommended Tailors")

    tailors = st.session_state.tailors
    orders = st.session_state.orders

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

    
    # 1. Identify Busy Tailors (One Order Per Tailor SOP)
    busy_tailor_ids = set()
    for o in orders:
        if o.status != "COMPLETED" and o.tailors_involved:
            for tid in o.tailors_involved:
                busy_tailor_ids.add(tid)
                
    # 2. Filter: Capacity < Max AND Not Busy
    available_tailors = [
        t for t in tailors 
        if t.current_workload < t.max_capacity and t.id not in busy_tailor_ids
    ]


    for tailor in available_tailors:
        with st.expander(f"{tailor.name}", expanded=False):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write("**Skills**")

                for skill, level in tailor.skill_vector.items():
                    # Skills are 1-10, progress expects 0.0-1.0
                    normalized_level = min(max(level / 10.0, 0.0), 1.0)
                    st.progress(normalized_level, text=f"{skill} ({level})")

                st.write(f"Reliability: {tailor.reliability_score}")
                st.write(
                    f"Workload: {tailor.current_workload}/{tailor.max_capacity}"
                )
                st.write(f"Availability: {tailor.availability_hours} hrs")
        st.session_state.selected_tailors.add(tailor.id)


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
        if st.button("Accept", type="primary"):
            st.session_state.assignment_mode = "QTY"
            st.rerun()

    with col2:
        if st.button("Reject & Choose Manually", use_container_width=True):
            st.session_state.selected_tailors.clear()
            st.session_state.assignment_mode = "MANUAL"
            st.rerun()
            
