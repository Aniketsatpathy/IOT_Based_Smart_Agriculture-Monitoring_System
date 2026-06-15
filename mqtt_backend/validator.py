import config
from logger import system_logger

def validate_payload(payload: dict) -> bool:
    """
    Validates the incoming JSON payload from the ESP32.
    Checks for missing fields, incorrect data types, and out-of-range sensor values.
    Returns True if valid, False otherwise.
    """
    required_fields = ["temperature", "humidity", "soil_moisture", "water_level", "light_intensity", "pump_status"]
    
    # 1. Check for missing fields
    for field in required_fields:
        if field not in payload:
            system_logger.error(f"Validation Failed: Missing required field '{field}'. Payload: {payload}")
            return False
            
    # 2. Validate Temperature
    try:
        temp = float(payload["temperature"])
        if not (config.VAL_TEMP_MIN <= temp <= config.VAL_TEMP_MAX):
            system_logger.error(f"Validation Failed: Temperature {temp} out of range [{config.VAL_TEMP_MIN}, {config.VAL_TEMP_MAX}]")
            return False
    except (ValueError, TypeError):
        system_logger.error("Validation Failed: Invalid datatype for temperature. Expected numeric float.")
        return False
        
    # 3. Validate Humidity
    try:
        hum = float(payload["humidity"])
        if not (config.VAL_HUM_MIN <= hum <= config.VAL_HUM_MAX):
            system_logger.error(f"Validation Failed: Humidity {hum} out of range [{config.VAL_HUM_MIN}, {config.VAL_HUM_MAX}]")
            return False
    except (ValueError, TypeError):
        system_logger.error("Validation Failed: Invalid datatype for humidity. Expected numeric float.")
        return False

    # 4. Validate Soil Moisture
    try:
        soil = int(payload["soil_moisture"])
        if not (config.VAL_SOIL_MIN <= soil <= config.VAL_SOIL_MAX):
            system_logger.error(f"Validation Failed: Soil Moisture {soil} out of range [{config.VAL_SOIL_MIN}, {config.VAL_SOIL_MAX}]")
            return False
    except (ValueError, TypeError):
        system_logger.error("Validation Failed: Invalid datatype for soil_moisture. Expected integer.")
        return False

    # 5. Validate Water Level
    try:
        water = int(payload["water_level"])
        if not (config.VAL_WATER_MIN <= water <= config.VAL_WATER_MAX):
            system_logger.error(f"Validation Failed: Water Level {water} out of range [{config.VAL_WATER_MIN}, {config.VAL_WATER_MAX}]")
            return False
    except (ValueError, TypeError):
        system_logger.error("Validation Failed: Invalid datatype for water_level. Expected integer.")
        return False

    # 6. Validate Light Intensity
    try:
        light = int(payload["light_intensity"])
        if not (config.VAL_LIGHT_MIN <= light <= config.VAL_LIGHT_MAX):
            system_logger.error(f"Validation Failed: Light Intensity {light} out of range [{config.VAL_LIGHT_MIN}, {config.VAL_LIGHT_MAX}]")
            return False
    except (ValueError, TypeError):
        system_logger.error("Validation Failed: Invalid datatype for light_intensity. Expected integer.")
        return False

    # 7. Validate Pump Status
    pump = str(payload["pump_status"]).upper()
    if pump not in ["ON", "OFF"]:
        system_logger.error(f"Validation Failed: Invalid pump status '{pump}'. Expected 'ON' or 'OFF'.")
        return False

    system_logger.info("Validation Passed.")
    return True
