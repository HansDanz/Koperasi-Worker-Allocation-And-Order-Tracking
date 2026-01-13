import streamlit as st
from utils.style_utils import render_tailwind
from UI_components.qc_dialog import update_progress_dialog
from models.order import Order
from UI_components.ml_assignment import assign_ml_dialog

def render_order_detail(order, tailor_lookup):
    """
    Renders the full details of an order, including tailor management, QC, and pickup confirmation.
    Intended to be shown in a full-page view, distinct from the summary card.
    """
    
    # --- Header Section ---
    st.markdown(f"## {order.product_name}")
    st.caption(f"Client: {order.client_name} | ID: {order.id}")

    # Inject CSS for Blue Primary Buttons and Red Secondary Buttons
    st.markdown("""
        <style>
        /* Force Primary (Action) Buttons to be Blue */
        div.stButton > button[kind="primary"] {
            background-color: #3b82f6 !important;
            border-color: #3b82f6 !important;
            color: white !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #2563eb !important;
            border-color: #2563eb !important;
        }
        div.stButton > button[kind="primary"]:focus {
            color: white !important;
        }

        /* Force Secondary (Back) Buttons to be Red */
        div.stButton > button[kind="secondary"] {
            border-color: #ef4444 !important;
            color: #ef4444 !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #dc2626 !important;
            color: #dc2626 !important;
            background-color: #fef2f2 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Status & Progress
    col_stat, col_prog = st.columns([1, 2])
    with col_stat:
        st.metric("Status", order.status)
        st.metric("Deadline", str(order.deadline_date))
        
    with col_prog:
        if hasattr(order, 'progress_pct'):
            progress = order.progress_pct
        else:
            progress = (order.quantity_completed / order.quantity_required) * 100 if order.quantity_required > 0 else 0
        
        st.write(f"**Workflow Progress**: {progress}%")
        st.progress(progress / 100)
        st.write(f"**Quantity**: {order.quantity_completed} / {order.quantity_required} pcs")

    st.divider()

    # --- Tailor Management Section ---
    st.subheader("🧵 Tailor Allocation & Progress")
    
    # 1. Assignment Action (If in Sewing and empty)
    if order.status == "SEWING" and not order.tailors_involved:
        st.info("No tailors assigned yet. Use the button below to allocate work.")
        if st.button("Assign Tailors", key=f"detail_assign_{order.id}", type="primary"):
            st.session_state.current_order = order
            st.session_state.assignment_mode = "ML" 
            st.rerun()
            
    # 2. Tailor List & Actions
    elif order.tailors_involved:
        
        # Grid layout for tailors
        for tailor_id, data in order.tailors_involved.items():
            tailor = tailor_lookup.get(tailor_id)
            name = tailor.name if tailor else f"Unknown ({tailor_id})"
            
            assigned, completed, picked_up = order.get_tailor_status(tailor_id)
            
            # Card for each tailor row
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 2, 2])
                
                with c1:
                    st.write(f"**{name}**")
                    if picked_up:
                        st.caption("✅ Material Picked Up")
                    else:
                        st.caption("⏳ Waiting for Pickup")
                        
                with c2:
                    st.write(f"Target: {assigned}")
                    st.write(f"Done: {completed}")
                    # Visual bar
                    if assigned > 0:
                        st.progress(completed/assigned)
                        
                with c3:
                    # Actions specific to this tailor
                    if not picked_up:
                         if st.button("Confirm Pickup", key=f"btn_pickup_{order.id}_{tailor_id}"):
                             order.confirm_pickup(tailor_id)
                             st.rerun()
                    else:
                        # QC Update is currently global/dialog based, but could be inline here.
                        # For consistency with previous dialog, let's keep using the dialog but maybe trigger it per tailor?
                        # The existing dialog allows selecting the tailor. 
                        # Let's provide a shortcut to the dialog or just a "Update" button.
                        pass 


        # Global Actions for this section
        st.divider()
        qc_col1, qc_col2 = st.columns([1, 4])
        with qc_col1:
             if st.button("Update QC / Progress", key="detail_qc_btn", type="primary"):
                 update_progress_dialog(order, tailor_lookup)
                 
    else:
        st.write("No tailors involved.")

    st.divider()
    
    # --- Workflow Actions ---
    # Advance Status
    if order.status != "COMPLETED":
        target_stage_idx = Order.STATUS_FLOW.index(order.status) + 1
        if target_stage_idx < len(Order.STATUS_FLOW):
            target_stage = Order.STATUS_FLOW[target_stage_idx]
            if st.button(f"Next Stage: {target_stage} ➡️", key=f"detail_next_{order.id}", type="primary"):
                if order.advance_status():
                    st.session_state.detail_order_id = None # Return to list after advancing? Or stay? 
                    # Usually better to return to list as status changed implies new phase
                    st.rerun()

    # Back Button (Styled Red via CSS injection below)
    # Inject CSS specific for the Back button (which is rendered last)
    st.markdown("""
        <style>
        div.stButton > button[kind="secondary"] {
            border-color: #ef4444;
            color: #ef4444;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #dc2626;
            color: #dc2626;
            background-color: #fef2f2;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Orders List", type="secondary"):
        st.session_state.detail_order_id = None
        st.rerun()
