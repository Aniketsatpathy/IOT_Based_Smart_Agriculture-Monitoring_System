import streamlit as st
import pandas as pd
import time
from datetime import datetime
from dashboard_utils import load_sensor_data, load_alerts_data

st.set_page_config(page_title="Alert Center", page_icon="⚠️", layout="wide")

st.title("🚨 Alert Center")
st.markdown("Monitor current active threshold violations and view historical alerts.")

# Data Load
df_sensors = load_sensor_data()
df_alerts = load_alerts_data()

# Latest metrics
latest = None
if not df_sensors.empty:
    latest = df_sensors.iloc[-1]

# Custom styling
st.markdown("""
    <style>
    .alert-card {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-weight: bold;
        font-size: 16px;
    }
    .alert-high {
        background-color: #FFEBEE;
        color: #C62828;
        border-left: 6px solid #E53935;
    }
    .alert-warning {
        background-color: #FFFDE7;
        color: #F57F17;
        border-left: 6px solid #FBC02D;
    }
    .alert-nominal {
        background-color: #E8F5E9;
        color: #2E7D32;
        border-left: 6px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Active Alerts
st.header("⚠️ Active Alerts")

active_alerts = []
if latest is not None:
    if latest["temperature"] > 35:
        active_alerts.append(("HIGH TEMPERATURE", "HIGH", f"Current temperature is {latest['temperature']}°C (Threshold: > 35°C)"))
    if latest["soil_moisture"] < 30:
        active_alerts.append(("LOW SOIL MOISTURE", "HIGH", f"Current soil moisture is {latest['soil_moisture']}% (Threshold: < 30%)"))
    if latest["water_level"] < 20:
        active_alerts.append(("LOW WATER LEVEL", "WARNING", f"Current water level is {latest['water_level']}% (Threshold: < 20%)"))
        
if active_alerts:
    for alert_type, severity, msg in active_alerts:
        if severity == "HIGH":
            st.markdown(f'<div class="alert-card alert-high">🔴 {alert_type} ALERT: {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-card alert-warning">🟡 {alert_type} ALERT: {msg}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-card alert-nominal">✅ ALL SYSTEMS OPERATING NORMALLY - NO ACTIVE ALERTS</div>', unsafe_allow_html=True)

# 2. Alert History
st.header("📜 Alert History Log")

if not df_alerts.empty:
    ts_col = "Timestamp" if "Timestamp" in df_alerts.columns else "timestamp"
    type_col = "Alert Type" if "Alert Type" in df_alerts.columns else "alert_type"
    severity_col = "Severity" if "Severity" in df_alerts.columns else "severity"
    val_col = "Sensor Value" if "Sensor Value" in df_alerts.columns else "sensor_value"
    
    # Sort history
    df_alerts_sorted = df_alerts.sort_values(ts_col, ascending=False)
    
    # Sidebar filters
    st.sidebar.subheader("Filter Options")
    alert_types_list = ["All"] + list(df_alerts_sorted[type_col].unique())
    selected_type = st.sidebar.selectbox("Alert Type", alert_types_list)
    
    severities_list = ["All"] + list(df_alerts_sorted[severity_col].unique())
    selected_severity = st.sidebar.selectbox("Severity", severities_list)
    
    # Apply filters
    filtered_df = df_alerts_sorted.copy()
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df[type_col] == selected_type]
    if selected_severity != "All":
        filtered_df = filtered_df[filtered_df[severity_col] == selected_severity]
        
    st.markdown(f"Showing **{len(filtered_df)}** recorded alerts.")
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("No historical alerts logged yet.")

# Auto refresh
time.sleep(5)
st.rerun()
