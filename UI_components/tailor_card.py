import streamlit as st

def render_tailor_card(tailor):
    with st.container(border=True):
        st.subheader(tailor.name)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Skills**")
            for skill, level in tailor.skill_vector.items():
                st.progress(level, text=skill)

        with col2:
            st.write("**Status**")
            st.write(f"Reliability: {tailor.reliability_score}")
            st.write(f"Workload: {tailor.current_workload}/{tailor.max_capacity}")
            st.write(f"Available hours: {tailor.availability_hours}")

        st.caption(f"Employed since: {tailor.employed_since}")
