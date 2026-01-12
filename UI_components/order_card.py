import streamlit as st

tailors = st.session_state.tailors

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
            if order.tailors_involved:
                for tailor_id, qty in order.tailors_involved.items():
                    tailor = tailor_lookup.get(tailor_id)

                    if tailor:
                        st.write(f"- {tailor.name}: {qty} pieces")
                    else:
                        st.write(f"- Unknown tailor (ID {tailor_id})")

            else:
                if st.button(label="Click Here to Assign 📋", key=f"assign_order_{order.id}"):
                    st.session_state.current_order = order
                    st.session_state.assignment_mode = "ML"
                    st.rerun()

