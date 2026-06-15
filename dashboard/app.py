import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime, timedelta

# Import custom sub-modules
from dashboard_utils import (
    load_sensor_data,
    load_alerts_data,
    load_pump_history,
    load_system_health,
    load_recent_events
)
from charts import (
    create_temperature_chart,
    create_humidity_chart,
    create_soil_moisture_chart,
    create_water_level_chart,
    create_light_intensity_chart
)
from metrics import (
    calculate_sensor_kpis,
    calculate_pump_kpis
)

# Page configuration
st.set_page_config(
    page_title="Smart Agriculture Platform",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: 800;
        color: #2E7D32;
        font-family: 'Outfit', sans-serif;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px;
        color: #555555;
        margin-bottom: 25px;
    }
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #1B5E20;
        margin-top: 15px;
        margin-bottom: 10px;
        border-bottom: 2px solid #E0E0E0;
        padding-bottom: 5px;
    }
    .alert-card {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .alert-high {
        background-color: #FFEBEE;
        color: #C62828;
        border-left: 5px solid #E53935;
    }
    .alert-warning {
        background-color: #FFFDE7;
        color: #F57F17;
        border-left: 5px solid #FBC02D;
    }
    .alert-nominal {
        background-color: #E8F5E9;
        color: #2E7D32;
        border-left: 5px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- LOAD DATA -----------------
df_sensors = load_sensor_data()
df_alerts = load_alerts_data()
df_pump = load_pump_history()
health = load_system_health()
events = load_recent_events(limit=15) # Show last 15 in summary page

# Get latest reading if available
latest = None
if not df_sensors.empty:
    latest = df_sensors.iloc[-1]

# ----------------- HEADER -----------------
st.markdown('<div class="main-title">Smart Agriculture Monitoring Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time Greenhouse and Farm Management Dashboard</div>', unsafe_allow_html=True)

# ----------------- ROW 1: CURRENT METRICS -----------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    temp_val = f"{latest['temperature']:.1f} °C" if latest is not None else "N/A"
    st.metric(label="🌡️ Temperature", value=temp_val)

with col2:
    hum_val = f"{latest['humidity']:.1f} %" if latest is not None else "N/A"
    st.metric(label="💧 Humidity", value=hum_val)

with col3:
    soil_val = f"{latest['soil_moisture']:.0f} %" if latest is not None else "N/A"
    st.metric(label="🌱 Soil Moisture", value=soil_val)

with col4:
    water_val = f"{latest['water_level']:.0f} %" if latest is not None else "N/A"
    st.metric(label="🪣 Water Level", value=water_val)

with col5:
    pump_status = "UNKNOWN"
    if latest is not None:
        pump_status = str(latest["pump_status"]).upper()
    
    # Render with color helper
    if pump_status == "ON":
        st.metric(label="🔌 Pump Status", value="ON ✅", delta="Active", delta_color="normal")
    elif pump_status == "OFF":
        st.metric(label="🔌 Pump Status", value="OFF 💤", delta="Idle", delta_color="inverse")
    else:
        st.metric(label="🔌 Pump Status", value="N/A")

# ----------------- ROW 2: ACTIVE ALERTS & SYSTEM HEALTH -----------------
st.markdown('<div class="section-header">Status & Diagnostics</div>', unsafe_allow_html=True)
col_alerts, col_health = st.columns(2)

with col_alerts:
    st.subheader("⚠️ Active Alerts")
    
    active_alerts = []
    if latest is not None:
        if latest["temperature"] > 35:
            active_alerts.append(("HIGH TEMPERATURE", "HIGH"))
        if latest["soil_moisture"] < 30:
            active_alerts.append(("LOW SOIL MOISTURE", "HIGH"))
        if latest["water_level"] < 20:
            active_alerts.append(("LOW WATER LEVEL", "WARNING"))
            
    if active_alerts:
        for alert_type, severity in active_alerts:
            if severity == "HIGH":
                st.markdown(f'<div class="alert-card alert-high">🔴 {alert_type} ALERT</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-card alert-warning">🟡 {alert_type} ALERT</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-card alert-nominal">✅ ALL SYSTEMS NOMINAL</div>', unsafe_allow_html=True)

with col_health:
    st.subheader("🖥️ System Health")
    
    # Calculate heartbeat and backend running state
    backend_running = False
    if "last_heartbeat" in health:
        try:
            hb_time = datetime.strptime(health["last_heartbeat"], "%Y-%m-%d %H:%M:%S")
            # If heartbeat is within 12 seconds, backend is running
            if datetime.now() - hb_time < timedelta(seconds=12):
                backend_running = True
        except Exception:
            pass
            
    # MQTT data timestamp warning check
    mqtt_warning = False
    last_msg_str = "N/A"
    if "last_message_time" in health and health["last_message_time"] != "N/A":
        last_msg_str = health["last_message_time"]
        try:
            msg_time = datetime.strptime(last_msg_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - msg_time > timedelta(seconds=60):
                mqtt_warning = True
        except Exception:
            pass
    elif latest is not None:
        # fallback to latest CSV record timestamp
        last_msg_str = latest["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        try:
            msg_time = latest["timestamp"]
            if datetime.now() - msg_time > timedelta(seconds=60):
                mqtt_warning = True
        except Exception:
            pass
            
    # Display Health Information
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if backend_running:
            st.success("Backend: RUNNING")
        else:
            st.error("Backend: OFFLINE")
            
        mqtt_status = health.get("mqtt_status", "DISCONNECTED")
        if mqtt_status == "CONNECTED" and backend_running:
            st.success("MQTT: CONNECTED")
        else:
            st.error("MQTT: DISCONNECTED")
            
    with col_h2:
        csv_status = health.get("csv_status", "UNKNOWN")
        if csv_status == "ACTIVE":
            st.success("CSV Storage: ACTIVE")
        else:
            st.error("CSV Storage: ERROR")
            
        st.info(f"Last MQTT Message: {last_msg_str}")
        
    if mqtt_warning:
        st.warning("⚠️ MQTT DATA NOT RECEIVED FOR > 60 SECONDS")

# ----------------- ROW 3: TEMPERATURE & HUMIDITY TRENDS -----------------
st.markdown('<div class="section-header">Environmental Trends</div>', unsafe_allow_html=True)
col_chart_temp, col_chart_hum = st.columns(2)

with col_chart_temp:
    st.plotly_chart(create_temperature_chart(df_sensors), use_container_width=True)

with col_chart_hum:
    st.plotly_chart(create_humidity_chart(df_sensors), use_container_width=True)

# ----------------- ROW 4: SOIL MOISTURE & WATER LEVEL TRENDS -----------------
col_chart_soil, col_chart_water = st.columns(2)

with col_chart_soil:
    st.plotly_chart(create_soil_moisture_chart(df_sensors), use_container_width=True)

with col_chart_water:
    st.plotly_chart(create_water_level_chart(df_sensors), use_container_width=True)

# ----------------- ROW 5: LIGHT INTENSITY TREND -----------------
st.plotly_chart(create_light_intensity_chart(df_sensors), use_container_width=True)

# ----------------- ROW 6: ANALYTICS KPIS -----------------
st.markdown('<div class="section-header">Analytics Summary (Today)</div>', unsafe_allow_html=True)

# Calculate sensor KPIs from today's data
today_str = datetime.now().strftime("%Y-%m-%d")
df_sensors_today = pd.DataFrame()
if not df_sensors.empty:
    df_sensors["date"] = df_sensors["timestamp"].dt.strftime("%Y-%m-%d")
    df_sensors_today = df_sensors[df_sensors["date"] == today_str]

kpis = calculate_sensor_kpis(df_sensors_today)
pump_kpis = calculate_pump_kpis(df_pump)

col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.metric(label="AVG TEMP", value=f"{kpis['avg_temp']:.1f} °C", help="Average temperature today")
    st.metric(label="MAX TEMP", value=f"{kpis['max_temp']:.1f} °C", help="Maximum temperature today")
    st.metric(label="MIN TEMP", value=f"{kpis['min_temp']:.1f} °C", help="Minimum temperature today")

with col_kpi2:
    st.metric(label="AVG HUMIDITY", value=f"{kpis['avg_hum']:.1f} %", help="Average humidity today")

with col_kpi3:
    st.metric(label="AVG SOIL MOISTURE", value=f"{kpis['avg_soil']:.1f} %", help="Average soil moisture today")
    st.metric(label="MIN SOIL MOISTURE", value=f"{kpis['min_soil']:.1f} %", help="Lowest soil moisture today")

with col_kpi4:
    st.metric(label="AVG WATER LEVEL", value=f"{kpis['avg_water']:.1f} %", help="Average water level today")
    st.metric(label="MIN WATER LEVEL", value=f"{kpis['min_water']:.1f} %", help="Lowest water level today")

with col_kpi5:
    st.metric(label="PUMP ACTIVATIONS", value=str(pump_kpis["activations_today"]), help="Total pump activations today")
    st.metric(label="TOTAL EVENTS", value=str(pump_kpis["total_events_today"]), help="Total pump start/stop events today")

# ----------------- ROW 7: PUMP ACTIVITY & RECENT EVENTS -----------------
st.markdown('<div class="section-header">Logs & Operations</div>', unsafe_allow_html=True)
col_pump_act, col_events = st.columns(2)

with col_pump_act:
    st.subheader("🔌 Pump Activity History")
    if not df_pump.empty:
        # Get latest 10 pump history records
        ts_col = "Timestamp" if "Timestamp" in df_pump.columns else "timestamp"
        status_col = "Pump Status" if "Pump Status" in df_pump.columns else "pump_status"
        df_pump_display = df_pump.sort_values(ts_col, ascending=False).head(10)
        
        # Display formatted table
        formatted_pump_history = []
        for _, row in df_pump_display.iterrows():
            time_formatted = row[ts_col].strftime("%I:%M %p")
            status = row[status_col].upper()
            status_symbol = "🟢 ON" if status == "ON" else "⚫ OFF"
            formatted_pump_history.append({"Time": time_formatted, "Status": status_symbol})
            
        st.table(pd.DataFrame(formatted_pump_history))
    else:
        st.info("No pump activities logged today.")

with col_events:
    st.subheader("📜 Recent System Events")
    if events:
        for time_str, event_desc in events:
            # Color event icon based on keywords
            icon = "⚪"
            if "Alert" in event_desc:
                icon = "🔴" if "High" in event_desc or "Low Soil" in event_desc else "🟡"
            elif "Activated" in event_desc:
                icon = "🟢"
            elif "Deactivated" in event_desc:
                icon = "⚫"
            elif "Reconnected" in event_desc or "connected" in event_desc.lower():
                icon = "🔵"
                
            st.markdown(f"**{time_str}** — {icon} {event_desc}")
    else:
        st.info("No system events logged recently.")

# ----------------- AUTO REFRESH -----------------
time.sleep(5)
st.rerun()
