import streamlit as st
from utils.auth_utils import check_auth
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Ensure login
check_auth()

st.title("Monthly Financial Report")

tailors = st.session_state.tailors
orders = st.session_state.orders

# --- 1. Date Filter ---
col_m, col_y = st.columns(2)
with col_m:
    # Get available months from data or default to current
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    current_month_idx = datetime.now().month - 1
    selected_month_name = st.selectbox("Select Month", month_names, index=current_month_idx)
    selected_month = month_names.index(selected_month_name) + 1

with col_y:
    current_year = datetime.now().year
    # Mock year range if needed, or simple input
    selected_year = st.number_input("Select Year", value=2025, step=1)

# --- 2. Data Aggregation ---
# Filter orders completed in this month/year
monthly_orders = []
total_income = 0
total_material_cost = 0
total_wages = 0

for order in orders:
    if not order.deadline_date:
        continue
        
    # Check if order belongs to selected period
    # Use deadline as the "Revenue Realization" date
    o_date = None
    if isinstance(order.deadline_date, str):
        try:
            o_date = datetime.strptime(order.deadline_date, "%Y-%m-%d")
        except:
            pass
    else:
        o_date = order.deadline_date # assume datetime.date
        
    if o_date and o_date.month == selected_month and o_date.year == selected_year:
        monthly_orders.append(order)
        
        # Financials
        # Revenue = Budget (Client Price)
        total_income += getattr(order, 'budget', 0)
        
        # Costs
        qty = order.quantity_completed
        mat_unit = getattr(order, 'material_cost_per_piece', 0)
        wage_unit = getattr(order, 'wage_per_piece', 0)
        
        total_material_cost += (mat_unit * qty)
        total_wages += (wage_unit * qty)

total_expenses = total_material_cost + total_wages
net_profit = total_income - total_expenses
margin = (net_profit / total_income * 100) if total_income > 0 else 0

# --- 3. Summary Cards ---
st.divider()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"Rp {total_income:,.0f}")
k2.metric("Total Expenses", f"Rp {total_expenses:,.0f}")
k3.metric("Net Profit", f"Rp {net_profit:,.0f}", delta=f"{margin:.1f}% Margin")
k4.metric("Orders Completed", len(monthly_orders))

st.divider()

# --- 4. Visualizations ---
if monthly_orders:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Income vs Expenses")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(["Income", "Expenses"], [total_income, total_expenses], color=["#4ade80", "#f87171"])
        ax.set_ylabel("IDR")
        st.pyplot(fig)
        
    with c2:
        st.subheader("Expense Breakdown")
        if total_expenses > 0:
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            ax2.pie([total_wages, total_material_cost], labels=["Wages", "Materials/Ops"], autopct='%1.1f%%', colors=["#60a5fa", "#fbbf24"])
            st.pyplot(fig2)
        else:
            st.info("No expenses recorded.")

    st.divider()
    
    # --- 5. Tailor Earnings (Wages) ---
    st.subheader("Tailor Monthly Wages")
    
    # Aggregate wages by tailor for this month's orders
    tailor_earnings = {}
    
    for order in monthly_orders:
        wage_unit = getattr(order, 'wage_per_piece', 0)
        # Using tailors_involved to distribute
        if order.tailors_involved:
             for tid, data in order.tailors_involved.items():
                 # Handle int or dict
                 completed = 0
                 if isinstance(data, dict):
                     completed = data.get("completed", 0)
                 else:
                     completed = 0 # If int, assuming legacy format without completion tracking?
                 
                 earning = completed * wage_unit
                 
                 # Resolve Name
                 t_name = tid
                 found_t = next((t for t in tailors if t.id == tid), None)
                 if found_t: t_name = found_t.name
                 
                 if t_name in tailor_earnings:
                     tailor_earnings[t_name] += earning
                 else:
                     tailor_earnings[t_name] = earning

    if tailor_earnings:
        # Sort top earners
        sorted_earnings = dict(sorted(tailor_earnings.items(), key=lambda item: item[1], reverse=True))
        
        # Viz
        st.bar_chart(pd.Series(sorted_earnings))
        
        # Detailed Table
        st.write("### Detailed Payroll Table")
        df_wages = pd.DataFrame(list(sorted_earnings.items()), columns=["Tailor", "Total Wage"])
        st.dataframe(
            df_wages.style.format({"Total Wage": "Rp {:,.0f}"}),
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("No completed orders found for this period.")