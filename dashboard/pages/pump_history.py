import streamlit as st
import pandas as pd
import time
from datetime import datetime
from dashboard_utils import load_pump_history
from metrics import calculate_pump_kpis

st.set_page_config(page_title="Pump Operations", page_icon="🔌", layout="wide")

st.title("🔌 Pump Activity History")
st.markdown("Track detailed operations of the irrigation pump, transitions, and daily activation statistics.")

# Load Data
df_pump = load_pump_history()

# Calculate stats
stats = calculate_pump_kpis(df_pump)

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Activations (Today)", value=str(stats["activations_today"]))
with col2:
    st.metric(label="Total Deactivations (Today)", value=str(stats["deactivations_today"]))
with col3:
    st.metric(label="Total Operations Today", value=str(stats["total_events_today"]))

st.markdown("---")
st.header("📋 Operation Log")

if not df_pump.empty:
    ts_col = "Timestamp" if "Timestamp" in df_pump.columns else "timestamp"
    status_col = "Pump Status" if "Pump Status" in df_pump.columns else "pump_status"
    
    # Sort descending (most recent first)
    df_pump_display = df_pump.sort_values(ts_col, ascending=False).copy()
    
    # Sidebar filter
    st.sidebar.subheader("Filter Status")
    status_filter = st.sidebar.selectbox("Filter by Status", ["All", "ON", "OFF"])
    
    if status_filter != "All":
        df_pump_display = df_pump_display[df_pump_display[status_col].astype(str).str.upper() == status_filter]
        
    st.markdown(f"Showing **{len(df_pump_display)}** operational records.")
    
    # Format for clean display
    formatted_list = []
    for _, row in df_pump_display.iterrows():
        dt_val = row[ts_col]
        # format dt_val depending on if it is pd.Timestamp or str
        if isinstance(dt_val, str):
            date_str = dt_val
        else:
            date_str = dt_val.strftime("%Y-%m-%d %H:%M:%S")
            
        status = str(row[status_col]).upper()
        symbol = "🟢 ON (Activated)" if status == "ON" else "⚫ OFF (Deactivated)"
        
        formatted_list.append({
            "Date/Time": date_str,
            "Operation": symbol
        })
        
    st.table(pd.DataFrame(formatted_list))
else:
    st.info("No pump activity records found. Perform irrigation tasks to create logs.")

# Auto refresh
time.sleep(5)
st.rerun()
