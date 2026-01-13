import streamlit as st
import pandas as pd

from utils.style_utils import render_tailwind
from utils.auth_utils import check_auth

# Ensure login
check_auth()

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

st.subheader("Payment Distribution Visualization")
st.bar_chart(df.set_index("Name")["Total Earnings (IDR)"])
