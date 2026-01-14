import streamlit as st
from utils.auth_utils import check_auth

check_auth()

from UI_components.tailor_card import render_tailor_card
from utils.helpers import add_tailor

st.title("Workers")

tailors = st.session_state.tailors

@st.dialog("Enter personal information of new tailor")
def new_tailor():
    name = st.text_input("Name")

    skill_vector = {
        "Cutting": st.slider("Cutting", 0.0, 10.0),
        "Sewing": st.slider("Sewing", 0.0, 10.0),
        "QC": st.slider("QC", 0.0, 10.0),
        }
    reliability_score = st.slider("Reliability Score", min_value=0.0, max_value=10.0)
    max_capacity = st.slider("Max. Capacity", min_value=1, step=1)
    current_workload = st.slider("Current Workload", min_value=1)
    availability_hours = st.slider("Availability Hours", min_value=1)
    employed_since = st.date_input("Employed since")
    if st.button("Submit"):
        add_tailor(name, skill_vector, reliability_score, max_capacity, current_workload, availability_hours, employed_since)
        st.success("Order added")
        st.rerun()
<<<<<<< Updated upstream

col1, col2, col3, col4 = st.columns(4)

with col4:
    if st.button(label = "+ New Tailor", type = "primary"):
        new_tailor()

for tailor in tailors:
    render_tailor_card(tailor)
=======
else:
    # --- List View ---
    @st.dialog("Enter personal information of new tailor")
    def new_tailor():
        name = st.text_input("Name")
    
        skill_vector = {
            "Cutting": st.slider("Cutting", 0.0, 10.0),
            "Sewing": st.slider("Sewing", 0.0, 10.0),
            "QC": st.slider("QC", 0.0, 10.0),
            }
        reliability_score = st.slider("Reliability Score", min_value=0.0, max_value=10.0)
        availability_hours = st.slider("Availability Hours", min_value=1)
        employed_since = st.date_input("Employed since")
        if st.button("Submit"):
            add_tailor(name, skill_vector, reliability_score, availability_hours, employed_since)
            st.success("Order added")
            st.rerun()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col4:
        if st.button(label = "+ New Tailor", type = "primary"):
            new_tailor()
    
    # Search Bar
    search_query = st.text_input("Search Workers", placeholder="Search by Name or ID", label_visibility="collapsed")
    
    # Filter & Sort
    filtered_tailors = tailors
    if search_query:
        search_query = search_query.lower()
        filtered_tailors = [
            t for t in tailors 
            if search_query in t.name.lower() or search_query in t.id.lower()
        ]
        
    # Sort by ID (Numeric part)
    filtered_tailors.sort(key=lambda x: int(x.id[1:]) if x.id.startswith('T') else 0)
    
    # Grid Layout for Cards
    cols = st.columns(2) # 2 Column Grid
    for i, tailor in enumerate(filtered_tailors):
        with cols[i % 2]:
            render_tailor_card(tailor, orders)
>>>>>>> Stashed changes
