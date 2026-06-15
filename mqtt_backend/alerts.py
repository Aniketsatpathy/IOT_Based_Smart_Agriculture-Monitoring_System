import config
from models import SensorData, AlertRecord
from logger import save_alert, system_logger
from utils import ensure_directory_exists
from event_logger import log_event

def check_and_process_alerts(sensor_data: SensorData) -> list:
    """
    Evaluates SensorData against configuration thresholds.
    Generates and saves AlertRecords to CSV and alert_log.txt if thresholds are crossed.
    Returns the list of generated alerts.
    """
    alerts_triggered = []
    timestamp = sensor_data.timestamp

    # 1. Check Soil Moisture
    if sensor_data.soil_moisture < config.THRESHOLD_SOIL_MOISTURE:
        alert = AlertRecord(
            timestamp=timestamp,
            alert_type="LOW SOIL MOISTURE",
            severity="HIGH",
            sensor_value=float(sensor_data.soil_moisture)
        )
        alerts_triggered.append(alert)
        log_event("Low Soil Moisture Alert")

    # 2. Check Temperature
    if sensor_data.temperature > config.THRESHOLD_TEMP_HIGH:
        alert = AlertRecord(
            timestamp=timestamp,
            alert_type="HIGH TEMPERATURE",
            severity="HIGH",
            sensor_value=float(sensor_data.temperature)
        )
        alerts_triggered.append(alert)
        log_event("High Temperature Alert")

    # 3. Check Water Level
    if sensor_data.water_level < config.THRESHOLD_WATER_LEVEL:
        alert = AlertRecord(
            timestamp=timestamp,
            alert_type="LOW WATER LEVEL",
            severity="WARNING",
            sensor_value=float(sensor_data.water_level)
        )
        alerts_triggered.append(alert)
        log_event("Low Water Level Alert")

    # Process and save alerts
    if alerts_triggered:
        ensure_directory_exists(config.LOG_ALERT)
        try:
            with open(config.LOG_ALERT, mode="a", encoding="utf-8") as f:
                for alert in alerts_triggered:
                    # Save to CSV
                    save_alert(alert)
                    # Write to plain-text log
                    log_line = f"[{alert.timestamp}] ALERT - Type: {alert.alert_type}, Severity: {alert.severity}, Value: {alert.sensor_value}\n"
                    f.write(log_line)
                    # Log system message
                    system_logger.warning(f"Alert Generated: {alert.alert_type} ({alert.severity}) with value {alert.sensor_value}")
        except Exception as e:
            system_logger.error(f"Failed to write to alert log file {config.LOG_ALERT}: {e}")

    return alerts_triggered
