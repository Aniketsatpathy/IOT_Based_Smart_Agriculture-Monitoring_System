import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "mqtt_backend"))

from subscriber import message_callback, initialize_system
import config
from logger import system_logger

def run_tests():
    print("=== STARTING BACKEND PIPELINE TEST ===")
    
    # 1. Initialize Directories and State
    initialize_system()
    
    # Define test payloads
    valid_payload_1 = {
        "temperature": 28.5,
        "humidity": 65.0,
        "soil_moisture": 42,
        "water_level": 75,
        "light_intensity": 83,
        "pump_status": "OFF"
    }

    valid_payload_2 = {
        "temperature": 38.2,      # High temperature (>35) -> Alert!
        "humidity": 55.4,
        "soil_moisture": 25,      # Low soil moisture (<30) -> Alert!
        "water_level": 15,       # Low water level (<20) -> Alert!
        "light_intensity": 10,
        "pump_status": "ON"       # Pump transition ON -> Save to pump history!
    }

    invalid_payload_missing = {
        "temperature": 25.0,
        "humidity": 50.0
        # Missing fields!
    }

    invalid_payload_range = {
        "temperature": 150.0,     # Out of range! (>80)
        "humidity": 60.0,
        "soil_moisture": 50,
        "water_level": 50,
        "light_intensity": 50,
        "pump_status": "OFF"
    }

    # Clean previous test run files to start fresh for verification
    for filepath in [config.CSV_SENSOR_DATA, config.CSV_ALERTS, config.CSV_PUMP_HISTORY, config.CSV_DAILY_SUMMARY]:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Removed previous test file: {filepath}")

    print("\n--- Test 1: Sending Valid Payload 1 ---")
    message_callback(config.TOPIC_SENSOR, valid_payload_1)

    print("\n--- Test 2: Sending Valid Payload 2 (Should trigger alerts & pump change) ---")
    message_callback(config.TOPIC_SENSOR, valid_payload_2)

    print("\n--- Test 3: Sending Invalid Payload (Missing fields - should be rejected) ---")
    message_callback(config.TOPIC_SENSOR, invalid_payload_missing)

    print("\n--- Test 4: Sending Invalid Payload (Out of range - should be rejected) ---")
    message_callback(config.TOPIC_SENSOR, invalid_payload_range)

    print("\n=== VERIFYING CREATED FILES ===")
    
    # Verify CSV files
    for filepath in [config.CSV_SENSOR_DATA, config.CSV_ALERTS, config.CSV_PUMP_HISTORY, config.CSV_DAILY_SUMMARY]:
        exists = os.path.exists(filepath)
        print(f"CSV File '{filepath}' exists: {exists}")
        if exists:
            print(f"Content of {filepath}:")
            with open(filepath, "r") as f:
                print(f.read().strip())
            print("-" * 40)

    # Verify Text Logs
    for filepath in [config.LOG_SYSTEM, config.LOG_ALERT, config.REPORT_ANALYTICS]:
        exists = os.path.exists(filepath)
        print(f"Text File '{filepath}' exists: {exists}")
        if exists:
            print(f"Last 10 lines of {filepath}:")
            with open(filepath, "r") as f:
                lines = f.readlines()
                print("".join(lines[-10:]).strip())
            print("-" * 40)

if __name__ == "__main__":
    run_tests()
