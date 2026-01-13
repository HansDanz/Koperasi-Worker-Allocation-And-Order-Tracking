import streamlit as st
from utils.auth_utils import check_auth
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from datetime import datetime, date

# Ensure login
check_auth()

st.title("Monthly Financial Report")

tailors = st.session_state.tailors
orders = st.session_state.orders

# --- Helper: Data Aggregation ---
def get_financials_for_period(order_list, target_month=None, target_year=None):
    """
    Returns (stats_dict, filtered_orders)
    """
    filtered = []
    income = 0
    mat_cost = 0
    wages = 0
    
    for order in order_list:
        if not order.deadline_date:
            continue
            
        o_date = None
        if isinstance(order.deadline_date, str):
            try:
                o_date = datetime.strptime(order.deadline_date, "%Y-%m-%d")
            except:
                pass
        else:
            o_date = order.deadline_date 
            
        # Filter Logic
        if target_month and target_year:
             if hasattr(o_date, 'month'):
                 if not (o_date.month == target_month and o_date.year == target_year):
                     continue
        
        filtered.append(order)
        
        income += getattr(order, 'budget', 0)
        
        qty = order.quantity_completed
        mat_unit = getattr(order, 'material_cost_per_piece', 0)
        wage_unit = getattr(order, 'wage_per_piece', 0)
        
        mat_cost += (mat_unit * qty)
        wages += (wage_unit * qty)

    expenses = mat_cost + wages
    net = income - expenses
    
    return {
        "income": income,
        "expenses": expenses,
        "wages": wages,
        "material_cost": mat_cost,
        "net_profit": net,
        "count": len(filtered)
    }, filtered

# --- Helper: Currency Formatter for Charts ---
def millions_formatter(x, pos):
    return f'{x*1e-6:.1f}M'

formatter = ticker.FuncFormatter(millions_formatter)

# --- 1. Global Filter ---
with st.container(border=True):
    col_m, col_y = st.columns(2)
    with col_m:
        month_names = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        # Default to July for demo since we know it has data, or current
        default_idx = 6 # July
        selected_month_name = st.selectbox("Select Month", month_names, index=default_idx)
        selected_month = month_names.index(selected_month_name) + 1

    with col_y:
        selected_year = st.number_input("Select Year", value=2025, step=1)

# --- 2. Calculate Current Period Stats ---
current_stats, current_orders = get_financials_for_period(orders, selected_month, selected_year)

# --- 3. Calculate Previous Period (MoM) ---
prev_month = selected_month - 1 if selected_month > 1 else 12
prev_year = selected_year if selected_month > 1 else selected_year - 1
prev_stats, _ = get_financials_for_period(orders, prev_month, prev_year)

def calc_delta(curr, prev):
    if prev == 0: return None
    return ((curr - prev) / prev) * 100

delta_income = calc_delta(current_stats["income"], prev_stats["income"])
delta_profit = calc_delta(current_stats["net_profit"], prev_stats["net_profit"])

# --- Tabs Structure ---
tab_overview, tab_insights, tab_payroll = st.tabs(["Overview", "Strategic Insights", "Worker Payroll"])

# === TAB 1: OVERVIEW ===
with tab_overview:
    
    # KPIs
    with st.container(border=True):
        st.subheader(f"Performance: {selected_month_name} {selected_year}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Revenue", f"Rp {current_stats['income']:,.0f}", 
                  delta=f"{delta_income:.1f}% vs last month" if delta_income is not None else "N/A")
        
        k2.metric("Total Expenses", f"Rp {current_stats['expenses']:,.0f}")
        
        margin = (current_stats['net_profit'] / current_stats['income'] * 100) if current_stats['income'] > 0 else 0
        k3.metric("Net Profit", f"Rp {current_stats['net_profit']:,.0f}", 
                  delta=f"{delta_profit:.1f}%" if delta_profit is not None else None)
                  
        k4.metric("Orders Completed", current_stats['count'])

    if current_orders:
        col_charts = st.columns(2)
        
        with col_charts[0]:
            with st.container(border=True):
                st.markdown("##### Income vs Expenses")
                fig, ax = plt.subplots(figsize=(5, 4))
                bars = ax.bar(["Income", "Expenses", "Profit"], 
                       [current_stats['income'], current_stats['expenses'], current_stats['net_profit']], 
                       color=["#4ade80", "#f87171", "#60a5fa"])
                
                # Format Y Axis
                ax.yaxis.set_major_formatter(formatter)
                ax.set_ylabel("Amount (Millions IDR)")
                
                # Add value labels on top
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height*1e-6:.1f}M',
                            ha='center', va='bottom', fontsize=9)
                
                st.pyplot(fig)
            
        with col_charts[1]:
            with st.container(border=True):
                st.markdown("##### Expense Breakdown")
                if current_stats['expenses'] > 0:
                    fig2, ax2 = plt.subplots(figsize=(5, 4))
                    ax2.pie([current_stats['wages'], current_stats['material_cost']], 
                            labels=["Wages", "Materials/Ops"], 
                            autopct='%1.1f%%', 
                            colors=["#60a5fa", "#fbbf24"],
                            startangle=90)
                    st.pyplot(fig2)
                else:
                    st.info("No expenses recorded.")
    else:
        st.info("No data available for this month.")

# === TAB 2: INSIGHTS ===
with tab_insights:
    
    with st.container(border=True):
        st.markdown("### Revenue Trend (Year to Date)")
        trend_data = []
        months_label = []
        revenues = []
        profits = []
        
        for m in range(1, 13):
            s, _ = get_financials_for_period(orders, m, selected_year)
            trend_data.append({"Month": month_names[m-1][:3], "Revenue": s["income"], "Profit": s["net_profit"]})
            months_label.append(month_names[m-1][:3])
            revenues.append(s["income"])
            profits.append(s["net_profit"])
        
        # Plot using Matplotlib for better control over formatting
        fig_trend, ax_trend = plt.subplots(figsize=(8, 4))
        ax_trend.plot(months_label, revenues, marker='o', label='Revenue', color='#4ade80', linewidth=2)
        ax_trend.plot(months_label, profits, marker='o', label='Profit', color='#60a5fa', linewidth=2)
        
        ax_trend.yaxis.set_major_formatter(formatter)
        ax_trend.set_ylabel("Amount (Millions IDR)")
        ax_trend.legend()
        ax_trend.grid(True, linestyle='--', alpha=0.6)
        
        st.pyplot(fig_trend)
    
    if current_orders:
        with st.container(border=True):
            st.markdown("### Profitability by Product Category (Current Month)")
            cat_stats = {} 
            
            for o in current_orders:
                cat = getattr(o, 'clothes_category', 'Unknown')
                rev = getattr(o, 'budget', 0)
                qty = o.quantity_completed
                cost = (getattr(o, 'material_cost_per_piece', 0) + getattr(o, 'wage_per_piece', 0)) * qty
                profit = rev - cost
                
                cat_stats[cat] = cat_stats.get(cat, 0) + profit
                    
            if cat_stats:
                 c_a, c_b = st.columns([1.5, 1])
                 with c_a:
                     fig3, ax3 = plt.subplots(figsize=(5,3))
                     bars3 = ax3.bar(cat_stats.keys(), cat_stats.values(), color="#818cf8")
                     ax3.set_title("Net Profit (IDR)")
                     
                     ax3.yaxis.set_major_formatter(formatter)
                     
                     for bar in bars3:
                        height = bar.get_height()
                        ax3.text(bar.get_x() + bar.get_width()/2., height,
                                f'{height*1e-6:.1f}M',
                                ha='center', va='bottom', fontsize=8)
                                
                     st.pyplot(fig3)
                 with c_b:
                     st.write("#### Details")
                     st.dataframe(pd.DataFrame(list(cat_stats.items()), columns=["Category", "Profit"]).style.format({"Profit": "Rp {:,.0f}"}), use_container_width=True)


# === TAB 3: PAYROLL ===
with tab_payroll:
    with st.container(border=True):
        st.subheader("Worker Wages Payout")
        
        if current_orders:
            # Aggregate wages
            tailor_earnings = {}
            for order in current_orders:
                wage_unit = getattr(order, 'wage_per_piece', 0)
                if order.tailors_involved:
                     for tid, data in order.tailors_involved.items():
                         if isinstance(data, dict):
                             completed = data.get("completed", 0)
                         else:
                             completed = 0
                         
                         earning = completed * wage_unit
                         
                         # Resolve Name
                         t_name = tid
                         found_t = next((t for t in tailors if t.id == tid), None)
                         if found_t: t_name = found_t.name
                         
                         tailor_earnings[t_name] = tailor_earnings.get(t_name, 0) + earning
            
            if tailor_earnings:
                sorted_earnings = dict(sorted(tailor_earnings.items(), key=lambda item: item[1], reverse=True))
                
                c_pay1, c_pay2 = st.columns([2, 1])
                with c_pay1:
                    st.dataframe(
                        pd.DataFrame(list(sorted_earnings.items()), columns=["Tailor", "Total Wage"])
                        .style.format({"Total Wage": "Rp {:,.0f}"}),
                        use_container_width=True,
                        hide_index=True
                    )
                with c_pay2:
                    st.write("Top Earners")
                    # Use a horizontal bar chart for better logic
                    fig_w, ax_w = plt.subplots(figsize=(4, 5))
                    names = list(sorted_earnings.keys())[:5] # Top 5
                    wages = list(sorted_earnings.values())[:5]
                    
                    y_pos = range(len(names))
                    ax_w.barh(y_pos, wages, align='center', color="#f472b6")
                    ax_w.set_yticks(y_pos)
                    ax_w.set_yticklabels(names)
                    ax_w.invert_yaxis()  # labels read top-to-bottom
                    ax_w.xaxis.set_major_formatter(formatter)
                    
                    st.pyplot(fig_w)
        else:
            st.info("No payroll data for this period.")