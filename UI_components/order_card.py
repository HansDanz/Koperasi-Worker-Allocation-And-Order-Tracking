import streamlit as st

tailors = st.session_state.tailors

def render_manual_assignment(order):
    st.subheader("Select Tailors Manually")

    available_tailors = [
        t for t in tailors
        if t.current_workload < t.max_capacity
    ]

    for tailor in available_tailors:
        with st.container(border=True):
            st.write(f"**{tailor.name}**")
            st.caption("Click to assign")

            if st.button("Select", key=f"manual_{tailor.id}"):
                st.session_state.selected_tailor = tailor
                st.session_state.assignment_mode = "MANUAL_QTY"
                st.rerun()



def render_order_card(order, tailor_lookup):
    with st.container(border=True):
        st.subheader(order.product_name)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Information**")
            st.write(f"Client: {order.client_name}")

        with col2:
            st.write("**Progress**")
            st.write(f"Status: {order.status}")
            st.progress(order.quantity_completed/order.quantity_required, text=f"{order.quantity_completed}/{order.quantity_required}")
            st.write("**Tailors involved:**")
            for tailor_id, qty in order.tailors_involved.items():
                tailor = tailor_lookup.get(tailor_id)

                if tailor:
                    st.write(f"- {tailor.name}: {qty} pieces")
                else:
                    st.write(f"- Unknown tailor (ID {tailor_id})")

            if order.tailors_involved == {}:
                if st.button(label="Click Here to Assign 📋", key=f"assign_order_{order.id}"):
                    st.session_state.current_order = order
                    st.session_state.assignment_mode = "ML"
                    st.rerun()

