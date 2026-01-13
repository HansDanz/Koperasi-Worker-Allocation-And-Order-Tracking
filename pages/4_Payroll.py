import streamlit as st
from utils.auth_utils import check_auth
import matplotlib.pyplot as plt

# Ensure login
check_auth()

import pandas as pd
from utils.style_utils import render_tailwind

st.title("Payroll & Income Dashboard")

tailors = st.session_state.tailors
orders = st.session_state.orders

# Calculate Earnings
data = []
for tailor in tailors:
    earnings = tailor.calculate_earnings(orders)
    data.append({
        "ID": tailor.id,
        "Name": tailor.name,
        "Total Earnings (IDR)": earnings,
        "Active Workload": tailor.current_workload
    })

df = pd.DataFrame(data)

# Summary Stats
total_payout = df["Total Earnings (IDR)"].sum()
avg_earning = df["Total Earnings (IDR)"].mean() if not df.empty else 0

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Payout Pending", f"Rp {total_payout:,.0f}")
with col2:
    st.metric("Average Earning per Tailor", f"Rp {avg_earning:,.0f}")

st.divider()

st.subheader("Tailor Earnings Breakdown")

# Display as a styled table or cards
# Using standard dataframe for detailed view, but could use cards for summary
st.dataframe(
    df.style.format({"Total Earnings (IDR)": "Rp {:,.0f}"}),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Financial Report")

col1, col2, col3 = st.columns(3)
with col1:
    #st.metric("Total Payout Pending", f"Rp {total_payout:,.0f}")
    st.write("Income")
    labels_income = ['Project A', 'Project B', 'Project C']
    sizes = [300000, 500000, 400000]
    # Calculate percentages and format labels
    labels_income_complete = [f"{label} (Rp{size})" for label, size in zip(labels_income, sizes)]
    fig, ax = plt.subplots()
    ax.pie(sizes,
        labels=labels_income_complete,  # Use formatted labels
        wedgeprops={'width': 0.4},
        labeldistance=1.15,
        textprops={'fontsize': 14, 'fontweight': 'bold'},
        startangle=90,  # Start from the top
        counterclock=False)   # Make slices go clockwise
    ax.axis('equal')
    st.pyplot(fig)

with col2:
    #st.metric("Average Earning per Tailor", f"Rp {avg_earning:,.0f}")

    st.write("Cost Total")
    labels_cost_total = ['Raw Materials', 'Distribution', 'Wages', 'Utilities']
    sizes = [300000, 500000, 400000, 100000]
    # Calculate percentages and format labels
    labels_cost_total_complete = [f"{label} (Rp{size})" for label, size in zip(labels_cost_total, sizes)]
    fig, ax = plt.subplots()
    ax.pie(sizes,
        labels=labels_cost_total_complete,  # Use formatted labels
        wedgeprops={'width': 0.4},
        labeldistance=1.15,
        textprops={'fontsize': 14, 'fontweight': 'bold'},
        startangle=90,  # Start from the top
        counterclock=False)   # Make slices go clockwise
    ax.axis('equal')
    st.pyplot(fig)
    
with col3:
    st.write("Net Cashflow")
    labels = ['In', 'Out']
    sizes = [30, 50]
    # Calculate percentages and format labels
    percentages = [f"{label} ({size/sum(sizes)*100:.1f}%)" for label, size in zip(labels, sizes)]
    
    fig, ax = plt.subplots()
    ax.pie(sizes,
        labels=percentages,  # Use formatted labels
        wedgeprops={'width': 0.4},
        labeldistance=1.15,
        textprops={'fontsize': 14, 'fontweight': 'bold'},
        startangle=90,  # Start from the top
        counterclock=False)   # Make slices go clockwise
    ax.axis('equal')
    st.pyplot(fig)

col4, col5 = st.columns(2)
with col4:
    st.write("Top 5 Earners")
    st.bar_chart(df.set_index("Name")["Total Earnings (IDR)"],y_label="Earnings",sort="-Total Earnings (IDR)")

with col5:
    st.metric("Gross Profit", f"{100*3000000/12000000:,.2f}%")