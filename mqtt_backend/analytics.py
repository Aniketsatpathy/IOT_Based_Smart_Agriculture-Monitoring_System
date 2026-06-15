import os
import pandas as pd
from datetime import datetime
import config
from logger import system_logger
from utils import get_current_date, ensure_directory_exists

def generate_analytics_report(target_date: str = None) -> bool:
    """
    Reads stored CSV historical files and computes summaries for target_date (default: today).
    Saves results in daily_summary.csv and creates a text report in outputs/analytics_report.txt.
    """
    if target_date is None:
        target_date = get_current_date()

    system_logger.info(f"Starting daily analytics processing for date: {target_date}")

    # Initialize default metric values
    avg_temp = 0.0
    avg_hum = 0.0
    avg_soil = 0.0
    avg_water = 0.0
    max_temp = 0.0
    min_soil = 100.0
    alert_count = 0
    pump_activations = 0
    has_data = False

    # 1. Process Sensor Data CSV
    if os.path.exists(config.CSV_SENSOR_DATA):
        try:
            df_sensor = pd.read_csv(config.CSV_SENSOR_DATA)
            if not df_sensor.empty and "timestamp" in df_sensor.columns:
                # Extract date substring (first 10 chars: YYYY-MM-DD)
                df_sensor["date"] = df_sensor["timestamp"].astype(str).str.slice(0, 10)
                df_filtered = df_sensor[df_sensor["date"] == target_date]

                if not df_filtered.empty:
                    avg_temp = float(df_filtered["temperature"].mean())
                    avg_hum = float(df_filtered["humidity"].mean())
                    avg_soil = float(df_filtered["soil_moisture"].mean())
                    avg_water = float(df_filtered["water_level"].mean())
                    max_temp = float(df_filtered["temperature"].max())
                    min_soil = float(df_filtered["soil_moisture"].min())
                    has_data = True
        except Exception as e:
            system_logger.error(f"Error reading sensor data for analytics calculation: {e}")
    else:
        system_logger.warning(f"Sensor data CSV file {config.CSV_SENSOR_DATA} does not exist yet.")

    # 2. Process Alerts CSV
    if os.path.exists(config.CSV_ALERTS):
        try:
            df_alerts = pd.read_csv(config.CSV_ALERTS)
            ts_col = "Timestamp" if "Timestamp" in df_alerts.columns else "timestamp"
            if not df_alerts.empty and ts_col in df_alerts.columns:
                df_alerts["date"] = df_alerts[ts_col].astype(str).str.slice(0, 10)
                df_filtered_alerts = df_alerts[df_alerts["date"] == target_date]
                alert_count = int(len(df_filtered_alerts))
        except Exception as e:
            system_logger.error(f"Error reading alerts CSV for analytics calculation: {e}")

    # 3. Process Pump History CSV
    if os.path.exists(config.CSV_PUMP_HISTORY):
        try:
            df_pump = pd.read_csv(config.CSV_PUMP_HISTORY)
            ts_col = "Timestamp" if "Timestamp" in df_pump.columns else "timestamp"
            status_col = "Pump Status" if "Pump Status" in df_pump.columns else "pump_status"
            if not df_pump.empty and ts_col in df_pump.columns:
                df_pump["date"] = df_pump[ts_col].astype(str).str.slice(0, 10)
                # Count activations where status is ON
                df_filtered_pump = df_pump[(df_pump["date"] == target_date) & (df_pump[status_col].astype(str).str.upper() == "ON")]
                pump_activations = int(len(df_filtered_pump))
        except Exception as e:
            system_logger.error(f"Error reading pump history CSV for analytics calculation: {e}")

    # 4. Save to daily_summary.csv
    summary_data = {
        "date": target_date,
        "avg_temperature": round(avg_temp, 2),
        "avg_humidity": round(avg_hum, 2),
        "avg_soil_moisture": round(avg_soil, 2),
        "avg_water_level": round(avg_water, 2),
        "max_temperature": round(max_temp, 2),
        "min_soil_moisture": round(min_soil, 2) if has_data else 0.0,
        "alert_count": alert_count,
        "pump_activations": pump_activations
    }

    ensure_directory_exists(config.CSV_DAILY_SUMMARY)
    try:
        if os.path.exists(config.CSV_DAILY_SUMMARY):
            df_summary = pd.read_csv(config.CSV_DAILY_SUMMARY)
            # Remove previous calculations for this specific date to update it
            if not df_summary.empty and "date" in df_summary.columns:
                df_summary = df_summary[df_summary["date"] != target_date]
            df_new = pd.DataFrame([summary_data])
            df_summary = pd.concat([df_summary, df_new], ignore_index=True)
        else:
            df_summary = pd.DataFrame([summary_data])
        
        df_summary.to_csv(config.CSV_DAILY_SUMMARY, index=False)
        system_logger.info("Daily summary CSV updated.")
    except Exception as e:
        system_logger.error(f"Error writing daily summary CSV: {e}")

    # 5. Format and save outputs/analytics_report.txt
    ensure_directory_exists(config.REPORT_ANALYTICS)
    try:
        report_content = f"""==================================================
IOT SMART AGRICULTURE - DAILY ANALYTICS REPORT
==================================================
Date: {target_date}
Generated At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
--------------------------------------------------
SENSOR METRICS:
- Average Temperature:    {avg_temp:.2f} °C
- Average Humidity:       {avg_hum:.2f} %
- Average Soil Moisture:  {avg_soil:.2f} %
- Average Water Level:    {avg_water:.2f} %
- Maximum Temperature:    {max_temp:.2f} °C
- Minimum Soil Moisture:  {(min_soil if has_data else 0.0):.2f} %

SYSTEM EVENTS:
- Total Alerts Generated: {alert_count}
- Pump Activations (ON):  {pump_activations}
==================================================
"""
        with open(config.REPORT_ANALYTICS, mode="w", encoding="utf-8") as f:
            f.write(report_content)
        system_logger.info(f"Analytics report successfully saved to: {config.REPORT_ANALYTICS}")
    except Exception as e:
        system_logger.error(f"Error writing analytics report file: {e}")

    return True


if __name__ == "__main__":
    # Execute manually for testing purposes
    generate_analytics_report()
