import os
import pandas as pd
import json
from datetime import datetime

SENSOR_DATA_PATH = "data/sensor_data.csv"
ALERTS_CSV_PATH = "data/alerts.csv"
PUMP_HISTORY_CSV_PATH = "data/pump_history.csv"
DAILY_SUMMARY_CSV_PATH = "data/daily_summary.csv"
SYSTEM_LOG_PATH = "outputs/system_log.txt"
SYSTEM_HEALTH_JSON_PATH = "data/system_health.json"

def load_sensor_data():
    if os.path.exists(SENSOR_DATA_PATH):
        try:
            df = pd.read_csv(SENSOR_DATA_PATH)
            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                return df
        except Exception:
            pass
    return pd.DataFrame(columns=["timestamp", "temperature", "humidity", "soil_moisture", "water_level", "light_intensity", "pump_status"])

def load_alerts_data():
    if os.path.exists(ALERTS_CSV_PATH):
        try:
            df = pd.read_csv(ALERTS_CSV_PATH)
            if not df.empty:
                # Support capitalized or lowercase Timestamp
                ts_col = "Timestamp" if "Timestamp" in df.columns else "timestamp"
                df[ts_col] = pd.to_datetime(df[ts_col])
                return df
        except Exception:
            pass
    return pd.DataFrame(columns=["Timestamp", "Alert Type", "Severity", "Sensor Value"])

def load_pump_history():
    if os.path.exists(PUMP_HISTORY_CSV_PATH):
        try:
            df = pd.read_csv(PUMP_HISTORY_CSV_PATH)
            if not df.empty:
                # Support capitalized or lowercase Timestamp
                ts_col = "Timestamp" if "Timestamp" in df.columns else "timestamp"
                df[ts_col] = pd.to_datetime(df[ts_col])
                return df
        except Exception:
            pass
    return pd.DataFrame(columns=["Timestamp", "Pump Status"])

def load_daily_summary():
    if os.path.exists(DAILY_SUMMARY_CSV_PATH):
        try:
            df = pd.read_csv(DAILY_SUMMARY_CSV_PATH)
            return df
        except Exception:
            pass
    return pd.DataFrame()

def load_system_health():
    if os.path.exists(SYSTEM_HEALTH_JSON_PATH):
        try:
            with open(SYSTEM_HEALTH_JSON_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def load_recent_events(limit=50):
    events = []
    if os.path.exists(SYSTEM_LOG_PATH):
        try:
            with open(SYSTEM_LOG_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in reversed(lines):
                if " - INFO - EVENT: " in line:
                    parts = line.split(" - INFO - EVENT: ")
                    if len(parts) == 2:
                        ts_str = parts[0].strip() # e.g. "2026-06-15 17:45:01,632"
                        event_text = parts[1].strip()
                        try:
                            # format check, extracting the time portion
                            dt = datetime.strptime(ts_str.split(",")[0], "%Y-%m-%d %H:%M:%S")
                            time_str = dt.strftime("%H:%M:%S")
                        except Exception:
                            # fallback: try splitting space/comma
                            try:
                                time_str = ts_str.split(" ")[1].split(",")[0]
                            except Exception:
                                time_str = ts_str
                        events.append((time_str, event_text))
                        if len(events) >= limit:
                            break
        except Exception:
            pass
    return events
