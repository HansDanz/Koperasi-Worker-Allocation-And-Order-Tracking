import streamlit as st
import pandas as pd
import sys
import os

# Ensure we can import from src
# We look for the 'src' folder in the nested structure as identified
src_path = os.path.join(os.getcwd(), 'GEO-2026-main', 'GEO-2026-main')
if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from src.model import TailorOracle
except ImportError:
    # Fallback or error handling if path is wrong
    st.error("Could not import TailorOracle. Please check the src folder structure.")
    TailorOracle = None

from utils.helpers import commit_assignment

@st.dialog("Suggested Assignment")
def assign_ml_dialog(order):
    st.subheader("Recommended Tailors (AI Powered)")

    tailors = st.session_state.tailors
    orders = st.session_state.orders

    # --- Initialize Model ---
    if "tailor_oracle" not in st.session_state and TailorOracle:
        oracle = TailorOracle()
        data_path = r"d:\GEO\Koperasi-Worker-Allocation-And-Order-Tracking\data\geo dummy -2.xlsx"
        try:
            df = pd.read_excel(data_path)
            oracle.fit(df)
            st.session_state.tailor_oracle = oracle
        except Exception as e:
            st.error(f"Failed to train AI model: {e}")
            st.session_state.tailor_oracle = None
    
    oracle = st.session_state.get("tailor_oracle")

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

    # 3. Predict & Rank
    ranked_tailors = []
    if oracle:
        for t in available_tailors:
            try:
                # Predict days for the FULL order quantity
                # We prioritize the model's requirements: Name, Clothes Type, Specialist, Qty
                specialty = t.skill_vector.get("specialty", "Generalist")
                pred_days = oracle.predict_one(t.name, order.clothes_type, order.quantity_required, specialty)
                ranked_tailors.append((pred_days, t))
            except Exception as e:
                # Fallback if prediction fails
                ranked_tailors.append((999.0, t))
        
        # Sort by Predicted Days (Ascending)
        ranked_tailors.sort(key=lambda x: x[0])
    else:
        # No AI, just keep original list with dummy score
        ranked_tailors = [(0.0, t) for t in available_tailors]

    # Limit to Top 5 Tailors (Default) - Let user adjust
    col_filter, col_spacer = st.columns([1, 1])
    with col_filter:
        num_tailors = st.slider(
            "Target Number of Tailors", 
            min_value=1, 
            max_value=min(20, len(ranked_tailors)), 
            value=5
        )
    
    top_ranked_tailors = ranked_tailors[:num_tailors]
    
    st.write(f"Assigning **{order.quantity_required} pcs** of **{order.clothes_type}**")
    
    if not top_ranked_tailors:
        st.warning("No available tailors found.")
    else:
        st.caption(f"Showing Top {num_tailors} AI Recommendations")

    # Header for the list
    header_col1, header_col2 = st.columns([0.1, 0.9])
    with header_col1:
        st.markdown("**Select**")
    with header_col2:
        st.markdown("**Tailor Details**")

    for days, tailor in top_ranked_tailors:
        
        # 1. Selection Column (Outside Expander for Visibility)
        c_check, c_info = st.columns([0.1, 0.9], vertical_alignment="top")
        
        # Checkbox Logic: Default to True if not in state
        chk_key = f"chk_ml_{tailor.id}"
        
        # If we haven't seen this checkbox in this session run, default it to True
        if chk_key not in st.session_state:
            st.session_state[chk_key] = True
            
        with c_check:
            is_checked = st.checkbox(
                "Select", 
                key=chk_key, 
                label_visibility="collapsed"
            )
            
        # Sync with selected_tailors set
        if is_checked:
            st.session_state.selected_tailors.add(tailor.id)
        elif tailor.id in st.session_state.selected_tailors:
            st.session_state.selected_tailors.remove(tailor.id)

        # 2. Details Column (Expander)
        with c_info:
            label = f"**{tailor.name}**"
            if oracle and days < 995: 
                label += f" | ⚡ Est. {days:.1f} Days"
            
            with st.expander(label, expanded=False):
                if oracle:
                        daily_rate = order.quantity_required / max(days, 0.001)
                        st.metric("Predicted Rate", f"{daily_rate:.1f} /day")
                st.write("**Skills**")
                for skill, level in tailor.skill_vector.items():
                    if isinstance(level, (int, float)):
                        normalized_level = min(max(level / 10.0, 0.0), 1.0)
                        st.progress(normalized_level, text=f"{skill} ({level})")
                    else:
                        st.write(f"**{skill.capitalize()}:** {level}")
                
                st.write(f"Reliability: {tailor.reliability_score}")
                st.write(f"Workload: {tailor.current_workload}/{tailor.max_capacity}")
                st.write(f"Availability: {tailor.availability_hours} hrs")

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Assign Selected", type="primary"):
            if not st.session_state.selected_tailors:
                st.error("Please select at least one tailor.")
            else:
                st.session_state.assignment_mode = "QTY"
                st.rerun()

    with col2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.selected_tailors.clear()
            st.session_state.assignment_mode = "MANUAL"
            st.rerun()
