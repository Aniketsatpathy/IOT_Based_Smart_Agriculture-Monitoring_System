import pandas as pd
from datetime import datetime

def calculate_sensor_kpis(df):
    """
    Calculates summary metrics from sensor data.
    """
    kpis = {
        "avg_temp": 0.0, "max_temp": 0.0, "min_temp": 0.0,
        "avg_hum": 0.0,
        "avg_soil": 0.0, "min_soil": 0.0,
        "avg_water": 0.0, "min_water": 0.0
    }
    if not df.empty:
        kpis["avg_temp"] = float(df["temperature"].mean())
        kpis["max_temp"] = float(df["temperature"].max())
        kpis["min_temp"] = float(df["temperature"].min())
        
        kpis["avg_hum"] = float(df["humidity"].mean())
        
        kpis["avg_soil"] = float(df["soil_moisture"].mean())
        kpis["min_soil"] = float(df["soil_moisture"].min())
        
        kpis["avg_water"] = float(df["water_level"].mean())
        kpis["min_water"] = float(df["water_level"].min())
    return kpis

def calculate_pump_kpis(df_pump):
    """
    Calculates pump statistics from pump history.
    """
    stats = {
        "activations_today": 0,
        "deactivations_today": 0,
        "total_events_today": 0
    }
    if not df_pump.empty:
        ts_col = "Timestamp" if "Timestamp" in df_pump.columns else "timestamp"
        status_col = "Pump Status" if "Pump Status" in df_pump.columns else "pump_status"
        
        today = datetime.now().strftime("%Y-%m-%d")
        df_pump["date"] = pd.to_datetime(df_pump[ts_col]).dt.strftime("%Y-%m-%d")
        df_today = df_pump[df_pump["date"] == today]
        
        stats["activations_today"] = int((df_today[status_col].astype(str).str.upper() == "ON").sum())
        stats["deactivations_today"] = int((df_today[status_col].astype(str).str.upper() == "OFF").sum())
        stats["total_events_today"] = len(df_today)
    return stats
