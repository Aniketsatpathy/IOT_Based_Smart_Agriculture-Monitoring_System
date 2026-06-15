import streamlit as st
import os
import pandas as pd
import time
from datetime import datetime, timedelta
from dashboard_utils import load_system_health, load_sensor_data

st.set_page_config(page_title="System Health Monitor", page_icon="🖥️", layout="wide")

st.title("🖥️ System Health Diagnostics")
st.markdown("Monitor the operational status of MQTT connections, storage paths, and the backend processor.")

health = load_system_health()
df_sensors = load_sensor_data()

# Calculate heartbeat and backend running state
backend_running = False
hb_diff_seconds = None
if "last_heartbeat" in health:
    try:
        hb_time = datetime.strptime(health["last_heartbeat"], "%Y-%m-%d %H:%M:%S")
        diff = datetime.now() - hb_time
        hb_diff_seconds = diff.total_seconds()
        # If heartbeat is within 12 seconds, backend is running
        if diff < timedelta(seconds=12):
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
elif not df_sensors.empty:
    latest = df_sensors.iloc[-1]
    last_msg_str = latest["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    try:
        msg_time = latest["timestamp"]
        if datetime.now() - msg_time > timedelta(seconds=60):
            mqtt_warning = True
    except Exception:
        pass

# Layout
col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.subheader("⚙️ Daemon Processor Status")
    if backend_running:
        st.success("Backend Service Status: RUNNING")
    else:
        st.error("Backend Service Status: OFFLINE")
        
    if hb_diff_seconds is not None:
        st.write(f"**Last Hearbeat:** {health['last_heartbeat']} ({int(hb_diff_seconds)} seconds ago)")
    else:
        st.write("**Last Heartbeat:** N/A")

    st.subheader("📡 MQTT Connectivity")
    mqtt_status = health.get("mqtt_status", "DISCONNECTED")
    if mqtt_status == "CONNECTED" and backend_running:
        st.success("Broker Connection: CONNECTED")
    else:
        st.error("Broker Connection: DISCONNECTED")
        
    st.write(f"**Broker Host:** broker.hivemq.com")
    st.write(f"**Broker Port:** 1883")
    st.write(f"**Topics Subscribed:** `smartfarm/sensors`, `smartfarm/alerts`, `smartfarm/pump`")
    st.write(f"**Last Packet Time:** {last_msg_str}")
    
    if mqtt_warning:
        st.warning("⚠️ MQTT DATA NOT RECEIVED FOR > 60 SECONDS")

with col_stat2:
    st.subheader("💾 File Database Statistics")
    
    csv_status = health.get("csv_status", "UNKNOWN")
    if csv_status == "ACTIVE":
        st.success("CSV Storage State: NOMINAL")
    else:
        st.error("CSV Storage State: FAULT")
        
    # File sizes
    paths = {
        "Sensor Data CSV": "data/sensor_data.csv",
        "Alerts CSV": "data/alerts.csv",
        "Pump History CSV": "data/pump_history.csv",
        "Daily Summary CSV": "data/daily_summary.csv",
        "System Log": "outputs/system_log.txt",
        "Alert Log": "outputs/alert_log.txt"
    }
    
    stats_list = []
    for label, path in paths.items():
        exists = os.path.exists(path)
        size_kb = os.path.getsize(path) / 1024 if exists else 0
        stats_list.append({
            "Database File": label,
            "Path": f"`{path}`",
            "Exists": "✅ Yes" if exists else "❌ No",
            "Size": f"{size_kb:.2f} KB" if exists else "N/A"
        })
        
    st.table(pd.DataFrame(stats_list))

# Auto refresh
time.sleep(5)
st.rerun()
