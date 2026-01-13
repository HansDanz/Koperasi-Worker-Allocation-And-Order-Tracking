
import streamlit as st
from utils.style_utils import render_tailwind

def render_tailor_card(tailor, orders=[]):
    skills_html = ""

    for skill, level in tailor.skill_vector.items():
        if isinstance(level, (int, float)):
            percentage = int(level * 10)
            skills_html += f"""
            <div class="mb-3">
                <div class="flex justify-between mb-1">
                    <span class="text-sm font-medium text-gray-700">{skill.replace('_',' ').title()}</span>
                    <span class="text-xs font-semibold text-gray-500">{percentage}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-indigo-600 h-2 rounded-full" style="width: {percentage}%"></div>
                </div>
            </div>
            """
        else:
            # String value (e.g. Specialty: "All")
            skills_html += f"""
            <div class="mb-3 flex justify-between items-center">
                 <span class="text-sm font-medium text-gray-700">{skill.capitalize()}</span>
                 <span class="px-2 py-1 text-xs font-bold text-white bg-indigo-500 rounded">{level}</span>
            </div>
            """

    # --- Insight Logic ---
    current_job = "Idle"
    status_color = "green"
    total_items_made = 0
    
    for order in orders:
        if order.tailors_involved and tailor.id in order.tailors_involved:
            # Check for active job
            if order.status != "COMPLETED" and current_job == "Idle":
                current_job = order.product_name
                status_color = "orange"
                
            # History Stats
            stats = order.get_tailor_status(tailor.id) # returns (assigned, completed, picked_up)
            # Handle return value flexibly just in case
            if isinstance(stats, tuple):
                 total_items_made += stats[1] # completed qty

    # Wrapper HTML (Inner content only, removed outer card styling)
    # The outer styling (border, shadow) is now handled by st.container, though we lose the hover effect.
    card_html = f"""
    <div class="font-sans">
        <div class="flex justify-between items-start mb-4">
            <div>
                <h3 class="text-xl font-bold text-gray-900">{tailor.name} <span class="text-sm font-normal text-gray-500">({tailor.id})</span></h3>
                <p class="text-xs text-gray-500 mt-1">Employed since: {tailor.employed_since}</p>
            </div>
            <span class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-green-400">
                Reliability: {tailor.reliability_score}
            </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Skills</h4>
                {skills_html}
            </div>
            
            <div>
                <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Status</h4>
                <div class="space-y-3">
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-600 block mb-1">Current Job</span>
                        <span class="text-sm font-bold text-{status_color}-600">{current_job}</span>
                    </div>
                    <div class="items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-600 block mb-1">Experience</span>
                        <span class="text-sm font-bold text-gray-900">{total_items_made} Items Made</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    with st.container(border=True):
        # Render content
        render_tailwind(card_html, height=340)
        
        # Action Button (Inside the container)
        if st.button("View Profile", key=f"btn_prof_{tailor.id}", use_container_width=True, type="primary"):
            st.session_state.detail_tailor_id = tailor.id
            st.rerun()
