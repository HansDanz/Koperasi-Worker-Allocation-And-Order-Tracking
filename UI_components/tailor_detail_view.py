import streamlit as st
import pandas as pd

def render_tailor_detail(tailor, orders):
    """
    Renders the full profile details of a tailor including personal info and project history.
    """
    
    # --- Profile Header ---
    c_img, c_info = st.columns([1, 4])
    
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
    
    with c_info:
        st.title(tailor.name)
        st.caption(f"ID: {tailor.id}")
        
        # Tags
        spec = tailor.skill_vector.get("specialty", "Generalist")
        st.markdown(f"**Specialty:** `{spec}`")
        
    st.divider()
    
    # --- Personal Info & Stats ---
    col1, col2, col3 = st.columns(3)
    
    # Logic for current job & total items
    current_job = "Idle"
    status_color = "green"
    total_items = 0
    
    for order in orders:
        if order.tailors_involved and tailor.id in order.tailors_involved:
            # Active Job Check
            if order.status != "COMPLETED" and current_job == "Idle":
                current_job = order.product_name
                status_color = "orange"
                
            # History Stats
            stats = order.get_tailor_status(tailor.id)
            if isinstance(stats, tuple):
                 total_items += stats[1] # completed qty
    
    with col1:
        st.subheader("Personal Info")
        st.write(f"**Age:** {getattr(tailor, 'age', '-')}")
        st.write(f"**Phone:** {getattr(tailor, 'phone', '-')}")
        st.write(f"**Address:**")
        st.caption(getattr(tailor, 'address', '-'))

    with col2:
        st.subheader("Performance")
        st.metric("Reliability", f"{tailor.reliability_score}/10")
        st.metric("Total Experience", f"{total_items} pcs")
        
    with col3:
        st.subheader("Current Status")
        st.metric("Job", current_job)
        if current_job != "Idle":
            st.caption("Focusing on active task") # SOP indicator
        else:
            st.caption("Ready for assignment")
        
    st.divider()

    # --- Work History ---
    st.subheader("📂 Project History")
    
    # Filter orders involved
    history = []
    
    for order in orders:
        if order.tailors_involved and tailor.id in order.tailors_involved:
            # Get stats
            stats = order.get_tailor_stats(tailor.id)
            assigned, completed, _ = order.get_tailor_status(tailor.id)
            
            history.append({
                "ID": order.id,
                "Start Date": order.start_date,
                "Project": order.product_name,
                "Category": getattr(order, 'clothes_category', '-'),
                "Role/Assigned": f"{completed}/{assigned} pcs",
                "Speed": f"{stats.get('hours_per_piece', '-')} hr/pc",
                "Days Needed": stats.get('days_needed', '-'),
                "Status": order.status
            })
            
    if history:
        # Sort by ID Ascending
        history.sort(key=lambda x: x["ID"])
        
        df_hist = pd.DataFrame(history)
        st.dataframe(
            df_hist, 
            column_config={
                "ID": st.column_config.NumberColumn("ID", format="%d"),
                "Start Date": st.column_config.DateColumn("Date"),
                "Project": st.column_config.TextColumn("Project Name"),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No work history found for this tailor.")

    st.divider()
    
    # Back Button
    if st.button("← Back to Tailors List"):
        st.session_state.detail_tailor_id = None
        st.rerun()
