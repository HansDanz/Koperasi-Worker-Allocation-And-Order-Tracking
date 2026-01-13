import streamlit as st
from utils.style_utils import render_tailwind
from UI_components.qc_dialog import update_progress_dialog
from models.order import Order



@st.dialog("Update Actual Cost")
def edit_cost_dialog(order):
    st.write(f"Update cost for **{order.product_name}**")
    st.info(f"Budget: IDR {getattr(order, 'budget', 0):,.0f}")
    
    current_cost = getattr(order, 'actual_cost', 0)
    new_cost = st.number_input("Actual Project Cost (IDR)", min_value=0, step=1000, value=current_cost)
    
    if st.button("Save", type="primary"):
        order.actual_cost = new_cost
        st.success("Cost updated!")
        st.rerun()


def render_order_card(order, tailor_lookup, trigger_rerun=None):
    """
    Renders an order card using Tailwind CSS with visual progress bar for the workflow.
    """
    # Inject Custom CSS for Blue Buttons (Tailwind #3b82f6) locally for this component area
    # Inject Custom CSS for Blue Buttons (Tailwind #3b82f6) locally for this component area
    # Removed broad CSS that was affecting global buttons (like Logout). 
    # Global styling is now handled in auth_utils.py.
    # We rely on type="primary" for the specific blue buttons.

    
    # Calculate progress for visual bar
    if hasattr(order, 'progress_pct'):
        progress = order.progress_pct
    else:
        progress = (order.quantity_completed / order.quantity_required) * 100 if order.quantity_required > 0 else 0
        
    status_colors = {
        "DRAFT": "gray",
        "PROOFING": "yellow",
        "MATERIAL_SOURCING": "blue",
        "CUTTING": "indigo",
        "DISTRIBUTION": "purple",
        "SEWING": "pink",
        "QC": "orange",
        "COMPLETED": "green"
    }
    


    color = status_colors.get(order.status, "gray")
    
    # Summary of tailors instead of full list
    tailor_count = len(order.tailors_involved) if order.tailors_involved else 0
    assigned_text = f"{tailor_count} Tailors Assigned" if tailor_count > 0 else "No Tailors Assigned"
    
    # Status Colors for border strip
    status_hex_colors = {
        "DRAFT": "#9ca3af", # gray-400
        "PROOFING": "#facc15", # yellow-400
        "MATERIAL_SOURCING": "#fb923c", # orange-400
        "CUTTING": "#f87171", # red-400
        "SEWING": "#c084fc", # purple-400
        "DISTRIBUTION": "#60a5fa", # blue-400
        "COMPLETED": "#4ade80" # green-400
    }
    hex_color = status_hex_colors.get(order.status, "#9ca3af")

    # Simplified HTML: Content only, no card container styles (handled by st.container)
    # Removing p-4 mb-4 border-l-4 shadow, etc. We will use a wrapper.
    card_content_html = f"""
    <div class="bg-white">
        <div class="flex justify-between items-start mb-2">
            <div>
                <h3 class="text-lg font-bold text-gray-800">{order.product_name}</h3>
                <p class="text-sm text-gray-500">{order.client_name}</p>
            </div>
            <span class="px-2 py-1 text-xs font-semibold rounded-full bg-{color}-100 text-{color}-800">
                {order.status or 'Unknown'}
            </span>
        </div>
        
        <div class="mb-3">
            <div class="flex justify-between text-xs text-gray-500 mb-1">
                <span>Workflow Progress</span>
                <span>{progress}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-1.5">
                <div class="bg-{color}-500 h-1.5 rounded-full" style="width: {progress}%"></div>
            </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4 text-sm mb-3">
            <div>
                <p class="text-gray-500 text-xs">Quantity</p>
                <p class="font-medium">{order.quantity_completed} / {order.quantity_required}</p>
            </div>
            <div>
                <p class="text-gray-500 text-xs">Deadline</p>
                <p class="font-medium">{getattr(order, 'deadline_date', 'N/A')}</p>
            </div>
        </div>
        
        <div class="mt-2 text-xs text-gray-500">
           {assigned_text}
        </div>
    </div>
    """
    
    # Native Streamlit Container acting as the Card
    with st.container(border=True):
        # Colored Strip (simulating the border-left)
        st.markdown(f"""
            <div style="background-color: {hex_color}; height: 4px; width: 100%; border-radius: 2px; margin-bottom: 12px;"></div>
        """, unsafe_allow_html=True)

        # Render Content via Iframe (Tailwind)
        # Height reduced because buttons are gone and padding is tight
        render_tailwind(card_content_html, height=160)
        
        # Native Buttons Footer
        c1, spacer, c2 = st.columns([3, 4, 3])
        with c1:
             if hasattr(order, 'advance_status'):
                  if order.status == "COMPLETED":
                       # Show cost if set, else show button
                       cost = getattr(order, 'actual_cost', 0)
                       if cost > 0:
                           st.caption(f"Actual Cost: **IDR {cost:,.0f}**")
                       else:
                           if st.button("Input Actual Cost", key=f"cost_{order.id}", type="primary", use_container_width=True):
                               edit_cost_dialog(order)
                  else:
                      target_stage_idx = Order.STATUS_FLOW.index(order.status) + 1
                      if target_stage_idx < len(Order.STATUS_FLOW):
                          target_stage = Order.STATUS_FLOW[target_stage_idx]
                          
                          # SOP Check: Only allow moving to DISTRIBUTION if quantity is fully completed
                          if target_stage == "DISTRIBUTION" and order.quantity_completed < order.quantity_required:
                               pass
                          else:
                              # Formatting
                              formatted_stage = target_stage.replace("_", " ").title()
                              # Primary button for Next
                              if st.button(f"Next: {formatted_stage}", key=f"adv_{order.id}", type="primary", use_container_width=True):
                                  if order.advance_status():
                                      st.rerun()

        with c2:
             if st.button("Details", key=f"manage_{order.id}", use_container_width=True):
                 st.session_state.detail_order_id = order.id
                 st.rerun()
