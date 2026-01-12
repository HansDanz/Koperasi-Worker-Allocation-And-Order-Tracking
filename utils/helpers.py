import streamlit as st
from models.order import Order
from models.tailor import Tailor

def add_order(product_name, client_name, quantity_required):
    new_id = max(order.id for order in st.session_state.orders) + 1

    new_order = Order(
        id=new_id,
        product_name=product_name,
        client_name=client_name,
        quantity_required=quantity_required,
    )

    st.session_state.orders.append(new_order)

def add_tailor(name, skill_vector, reliability_score, max_capacity, current_workload, availability_hours, employed_since):
    new_id = max(order.id for order in st.session_state.orders) + 1

    new_tailor = Tailor(
        id=new_id,
        name=name,
        skill_vector=skill_vector,
        reliability_score=reliability_score,
        max_capacity = max_capacity,
        current_workload = current_workload,
        availability_hours=availability_hours,
        employed_since=employed_since,
    )

    st.session_state.tailors.append(new_tailor)

def commit_assignment(order, allocation):
    order.tailors_involved = allocation