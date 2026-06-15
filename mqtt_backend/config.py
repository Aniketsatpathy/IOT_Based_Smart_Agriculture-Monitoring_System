# ===== MQTT CONFIGURATION =====
BROKER = "broker.hivemq.com"
PORT = 1883
KEEPALIVE = 60

# ===== MQTT TOPICS =====
TOPIC_SENSOR = "smartfarm/sensors"
TOPIC_ALERTS = "smartfarm/alerts"
TOPIC_PUMP = "smartfarm/pump"

# ===== FILE PATHS =====
CSV_SENSOR_DATA = "data/sensor_data.csv"
CSV_ALERTS = "data/alerts.csv"
CSV_PUMP_HISTORY = "data/pump_history.csv"
CSV_DAILY_SUMMARY = "data/daily_summary.csv"

LOG_SYSTEM = "outputs/system_log.txt"
LOG_ALERT = "outputs/alert_log.txt"
REPORT_ANALYTICS = "outputs/analytics_report.txt"

# ===== THRESHOLD VALUES =====
THRESHOLD_SOIL_MOISTURE = 30  # Low moisture alert threshold (%)
THRESHOLD_TEMP_HIGH = 35       # High temperature alert threshold (°C)
THRESHOLD_WATER_LEVEL = 20    # Low water level alert threshold (%)

# ===== DATA VALIDATION LIMITS =====
VAL_TEMP_MIN = -20.0
VAL_TEMP_MAX = 80.0
VAL_HUM_MIN = 0.0
VAL_HUM_MAX = 100.0
VAL_SOIL_MIN = 0
VAL_SOIL_MAX = 100
VAL_WATER_MIN = 0
VAL_WATER_MAX = 100
VAL_LIGHT_MIN = 0
VAL_LIGHT_MAX = 100

# ===== RECONNECT CONFIGURATION =====
RECONNECT_DELAY_MIN = 1
RECONNECT_DELAY_MAX = 120
