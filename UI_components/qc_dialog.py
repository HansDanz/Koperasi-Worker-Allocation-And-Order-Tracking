import streamlit as st

@st.dialog("Update Tailor Progress (QC)")
def update_progress_dialog(order, tailor_lookup):
    st.write(f"**Order:** {order.product_name}")
    st.write(f"**Client:** {order.client_name}")
    st.divider()
    
    
    # Inject CSS for Blue Primary Buttons in Dialog
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
    
    if not order.tailors_involved:
        st.warning("No tailors assigned to this order yet.")
        if st.button("Close"):
            st.rerun()
        return

    st.write("Record completed pieces for each tailor:")
    
    # We need to manage state for inputs, but since dialog reruns on interaction, 
    # capturing inputs and submitting one by one or in bulk is better.
    # Let's do one by one for simplicity or a form.
    
    with st.form("qc_form"):
        updates = {}
        for tailor_id, data in order.tailors_involved.items():
            tailor = tailor_lookup.get(tailor_id)
            name = tailor.name if tailor else f"Unknown ({tailor_id})"
            
            # Handle data structure normalization locally if needed (though model does it)
            if isinstance(data, int):
                assigned = data
                completed = 0
            else:
                assigned = data.get("assigned", 0)
                completed = data.get("completed", 0)
            
            remaining = assigned - completed
            
            st.markdown(f"**{name}**")
            cols = st.columns(3)
            cols[0].caption(f"Assigned: {assigned}")
            cols[1].caption(f"Completed: {completed}")
            
            # Input for NEWLY completed items
            if remaining > 0:
                val = cols[2].number_input(
                    f"Add Completed (Max {remaining})", 
                    min_value=0, 
                    max_value=remaining, 
                    key=f"qc_{order.id}_{tailor_id}",
                    label_visibility="collapsed"
                )
                if val > 0:
                    updates[tailor_id] = val
            else:
                cols[2].caption("All Set ✅")
            
            st.divider()
            
        if st.form_submit_button("Update Progress", type="primary"):
            if not updates:
                st.info("No changes to update.")
            else:
                success_count = 0
                for tid, qty in updates.items():
                    if order.update_tailor_progress(tid, qty):
                        success_count += 1
                
                if success_count > 0:
                    st.success(f"Updated progress for {success_count} tailors!")
                    st.rerun()
                else:
                    st.error("Failed to update status.")
