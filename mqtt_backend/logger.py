import os
import csv
import logging
import sys
from utils import ensure_directory_exists
import config
from models import SensorData, AlertRecord, PumpRecord

# Ensure directories exist for files
ensure_directory_exists(config.LOG_SYSTEM)

# Setup Logging
system_logger = logging.getLogger("SmartFarmBackend")
system_logger.setLevel(logging.INFO)

# Avoid adding duplicate handlers if logger is imported multiple times
if not system_logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler
    file_handler = logging.FileHandler(config.LOG_SYSTEM, encoding="utf-8")
    file_handler.setFormatter(formatter)
    system_logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    system_logger.addHandler(console_handler)


def append_to_csv(file_path: str, headers: list, data: dict):
    """
    Appends a row to a CSV file. If the file does not exist, it is created with headers.
    """
    ensure_directory_exists(file_path)
    file_exists = os.path.exists(file_path)
    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        system_logger.error(f"Failed to write to CSV file {file_path}: {e}")


def save_sensor_data(sensor_data: SensorData):
    """
    Saves validated sensor data into data/sensor_data.csv.
    """
    headers = ["timestamp", "temperature", "humidity", "soil_moisture", "water_level", "light_intensity", "pump_status"]
    append_to_csv(config.CSV_SENSOR_DATA, headers, sensor_data.to_dict())
    system_logger.info("Sensor data successfully saved to CSV.")


def save_alert(alert_record: AlertRecord):
    """
    Saves a generated alert record into data/alerts.csv.
    """
    headers = ["Timestamp", "Alert Type", "Severity", "Sensor Value"]
    append_to_csv(config.CSV_ALERTS, headers, alert_record.to_dict())
    system_logger.info(f"Alert logged to CSV: {alert_record.alert_type} - {alert_record.severity}")


def save_pump_status(pump_record: PumpRecord):
    """
    Saves a pump transition record into data/pump_history.csv.
    """
    headers = ["Timestamp", "Pump Status"]
    data = {
        "Timestamp": pump_record.timestamp,
        "Pump Status": pump_record.pump_status
    }
    append_to_csv(config.CSV_PUMP_HISTORY, headers, data)
    system_logger.info(f"Pump status change logged to CSV: {pump_record.pump_status}")
