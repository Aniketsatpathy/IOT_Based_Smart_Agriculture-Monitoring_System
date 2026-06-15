import json
import os
import datetime
from utils import ensure_directory_exists
import config

SYSTEM_HEALTH_JSON_PATH = "data/system_health.json"

def update_system_health(mqtt_status: str, last_message_time: str = None):
    """
    Updates the system health file with current status and heartbeat.
    """
    ensure_directory_exists(SYSTEM_HEALTH_JSON_PATH)
    
    # Read existing data to preserve last_message_time if not provided
    data = {}
    if os.path.exists(SYSTEM_HEALTH_JSON_PATH):
        try:
            with open(SYSTEM_HEALTH_JSON_PATH, "r") as f:
                data = json.load(f)
        except Exception:
            pass
            
    data["last_heartbeat"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["mqtt_status"] = mqtt_status
    if last_message_time:
        data["last_message_time"] = last_message_time
    elif "last_message_time" not in data:
        data["last_message_time"] = "N/A"
        
    # Check CSV Status by verifying write capability
    csvs = [config.CSV_SENSOR_DATA, config.CSV_ALERTS, config.CSV_PUMP_HISTORY]
    csv_ok = True
    for csv_file in csvs:
        if os.path.exists(csv_file):
            try:
                # Test write/append permission
                with open(csv_file, "a"):
                    pass
            except Exception:
                csv_ok = False
                break
    data["csv_status"] = "ACTIVE" if csv_ok else "ERROR"
    data["backend_status"] = "RUNNING"
    
    try:
        with open(SYSTEM_HEALTH_JSON_PATH, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass
