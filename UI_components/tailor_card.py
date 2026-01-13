
import streamlit as st
from utils.style_utils import render_tailwind

def render_tailor_card(tailor):
    skills_html = ""

    for skill, level in tailor.skill_vector.items():
        percentage = int(level * 10)
        skills_html += f"""
        <div class="mb-3">
            <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-gray-700">{skill}</span>
                <span class="text-xs font-semibold text-gray-500">{percentage}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-indigo-600 h-2 rounded-full" style="width: {percentage}%"></div>
            </div>
        </div>
        """

    card_html = f"""
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-300 font-sans">
        <div class="flex justify-between items-start mb-4">
            <div>
                <h3 class="text-xl font-bold text-gray-900">{tailor.name}</h3>
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
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-600">Workload</span>
                        <span class="text-sm font-bold text-gray-900">{tailor.current_workload} / {tailor.max_capacity}</span>
                    </div>
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <span class="text-sm text-gray-600">Availability</span>
                        <span class="text-sm font-bold text-gray-900">{tailor.availability_hours} hrs</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Render with sufficient height to avoid scrollbars
    render_tailwind(card_html, height=280)
