import time
import os
import pandas as pd
import config
from utils import ensure_directory_exists, get_current_timestamp, get_current_date
from models import SensorData, PumpRecord
from validator import validate_payload
from logger import save_sensor_data, save_pump_status, system_logger
from alerts import check_and_process_alerts
from analytics import generate_analytics_report
from mqtt_handler import MQTTClientHandler

# Track previous pump status to log state changes
previous_pump_status = None

def get_last_pump_status() -> str:
    """
    Attempts to read the last known pump status from the sensor data CSV file to avoid redundant logs.
    """
    if os.path.exists(config.CSV_SENSOR_DATA):
        try:
            df = pd.read_csv(config.CSV_SENSOR_DATA)
            if not df.empty and "pump_status" in df.columns:
                return str(df["pump_status"].iloc[-1]).upper()
        except Exception as e:
            system_logger.warning(f"Could not load last pump status from CSV: {e}")
    return None

def message_callback(topic: str, payload: dict):
    """
    Callback triggered when an MQTT message arrives. Runs the payload through the data processing pipeline.
    """
    global previous_pump_status

    if topic == config.TOPIC_SENSOR:
        system_logger.info(f"New sensor payload received on topic '{topic}'. Processing...")

        # 1. Data Validation
        if not validate_payload(payload):
            system_logger.error("Sensor data payload validation failed. Message discarded.")
            return

        # 2. Parse into Data Model
        timestamp = get_current_timestamp()
        sensor_data = SensorData.from_dict(payload, timestamp)

        # 3. Persist Sensor Data to CSV
        save_sensor_data(sensor_data)

        # Update health message time
        from system_health import update_system_health
        update_system_health("CONNECTED", last_message_time=timestamp)

        # 4. Evaluate and Process Alerts
        check_and_process_alerts(sensor_data)

        # 5. Detect and log Pump State Transitions
        current_pump_status = sensor_data.pump_status
        if current_pump_status != previous_pump_status:
            system_logger.info(f"Pump transition detected: {previous_pump_status} -> {current_pump_status}")
            pump_record = PumpRecord(
                timestamp=timestamp,
                pump_status=current_pump_status,
                soil_moisture=sensor_data.soil_moisture,
                water_level=sensor_data.water_level
            )
            save_pump_status(pump_record)
            
            # Log event
            from event_logger import log_event
            if current_pump_status == "ON":
                log_event("Pump Activated")
            else:
                log_event("Pump Deactivated")
                
            previous_pump_status = current_pump_status

        # 6. Re-calculate analytics and update summary reports
        try:
            generate_analytics_report(get_current_date())
        except Exception as e:
            system_logger.error(f"Failed to generate analytics report: {e}")

    else:
        # Fallback/extension logs for non-sensor topics
        system_logger.info(f"Received message on topic '{topic}': {payload}")


def initialize_system():
    """
    Ensures directory structure is in place and restores initial state variables.
    """
    global previous_pump_status

    system_logger.info("Initializing IoT Smart Farm Backend...")

    # Auto-create all storage and log paths
    ensure_directory_exists(config.CSV_SENSOR_DATA)
    ensure_directory_exists(config.CSV_ALERTS)
    ensure_directory_exists(config.CSV_PUMP_HISTORY)
    ensure_directory_exists(config.CSV_DAILY_SUMMARY)
    ensure_directory_exists(config.LOG_SYSTEM)
    ensure_directory_exists(config.LOG_ALERT)
    ensure_directory_exists(config.REPORT_ANALYTICS)

    # Restore initial state
    previous_pump_status = get_last_pump_status()
    if previous_pump_status:
        system_logger.info(f"Restored last known pump status: '{previous_pump_status}'")
    else:
        system_logger.info("No prior pump status found. Initializing status tracking as None.")
    
    from system_health import update_system_health
    update_system_health("DISCONNECTED")


def main():
    initialize_system()

    # Create MQTT client handler
    handler = MQTTClientHandler(message_callback=message_callback)

    try:
        handler.connect()
        handler.start()

        system_logger.info("Backend subscriber is running. Press Ctrl+C to terminate.")
        # Keep main thread alive and update health heartbeat
        counter = 0
        from system_health import update_system_health
        while True:
            time.sleep(1)
            counter += 1
            if counter >= 5:
                # Update system health heartbeat
                mqtt_stat = "CONNECTED" if handler.client.is_connected() else "DISCONNECTED"
                update_system_health(mqtt_stat)
                counter = 0

    except KeyboardInterrupt:
        system_logger.info("Keyboard interrupt received. Shutting down system...")
    except Exception as e:
        system_logger.critical(f"Fatal unhandled exception: {e}", exc_info=True)
    finally:
        handler.stop()
        # Set backend status to offline
        try:
            import json
            from system_health import SYSTEM_HEALTH_JSON_PATH
            if os.path.exists(SYSTEM_HEALTH_JSON_PATH):
                with open(SYSTEM_HEALTH_JSON_PATH, "r") as f:
                    data = json.load(f)
                data["backend_status"] = "OFFLINE"
                data["mqtt_status"] = "DISCONNECTED"
                with open(SYSTEM_HEALTH_JSON_PATH, "w") as f:
                    json.dump(data, f, indent=4)
        except Exception:
            pass
        system_logger.info("Backend service stopped.")

if __name__ == "__main__":
    main()
