#include <ArduinoJson.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <WiFi.h>

#include "config.h"

// =======================
// WiFi
// =======================

const char *ssid = "Wokwi-GUEST";
const char *password = "";

// =======================
// Objects
// =======================

WiFiClient espClient;
PubSubClient mqtt(espClient);
DHT dht(DHT_PIN, DHT22);

// =======================
// Variables
// =======================

String pumpStatus = "OFF";

// =======================
// MQTT Connection
// =======================

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.println("Connecting MQTT...");

    if (mqtt.connect("ESP32SmartFarm")) {
      Serial.println("MQTT Connected");
    } else {
      Serial.println("Retrying...");
      delay(2000);
    }
  }
}

// =======================
// Setup
// =======================

void setup() {
  Serial.begin(115200);

  pinMode(RELAY_PIN, OUTPUT);

  dht.begin();

  WiFi.begin(ssid, password);

  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println();
  Serial.println("WiFi Connected");

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
}

// =======================
// Loop
// =======================

void loop() {
  if (!mqtt.connected()) {
    connectMQTT();
  }

  mqtt.loop();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // ==========================
  // Read Analog Sensors
  // ==========================

  int soilRaw = analogRead(SOIL_PIN);
  int waterRaw = analogRead(WATER_PIN);
  int lightRaw = analogRead(LDR_PIN);

  // Convert to %

  int soil = map(soilRaw, 0, 4095, 0, 100);

  int water = map(waterRaw, 0, 4095, 0, 100);

  int light = map(lightRaw, 0, 4095, 100, 0);

  // ==========================
  // Irrigation Logic
  // ==========================

  if (soil < 30 && water > 20) {
    digitalWrite(RELAY_PIN, HIGH);
    pumpStatus = "ON";
  } else {
    digitalWrite(RELAY_PIN, LOW);
    pumpStatus = "OFF";
  }

  // ==========================
  // Alerts
  // ==========================

  String alertMessage = "";

  if (soil < 30) {
    alertMessage += "Low Soil Moisture | ";
  }

  if (temperature > 35) {
    alertMessage += "High Temperature | ";
  }

  if (water < 20) {
    alertMessage += "Low Water Level | ";
  }

  // ==========================
  // JSON Payload
  // ==========================

  StaticJsonDocument<512> doc;

  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["soil_moisture"] = soil;
  doc["water_level"] = water;
  doc["light_intensity"] = light;
  doc["pump_status"] = pumpStatus;

  char payload[512];

  serializeJson(doc, payload);

  mqtt.publish(TOPIC_SENSOR, payload);

  // ==========================
  // Publish Alert
  // ==========================

  if (alertMessage.length() > 0) {
    mqtt.publish(TOPIC_ALERTS, alertMessage.c_str());
  }

  mqtt.publish(TOPIC_PUMP, pumpStatus.c_str());

  // ==========================
  // Serial Output
  // ==========================

  Serial.println();
  Serial.println("========== SMART FARM ==========");

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Humidity: ");
  Serial.println(humidity);

  Serial.print("Soil Moisture: ");
  Serial.println(soil);

  Serial.print("Water Level: ");
  Serial.println(water);

  Serial.print("Light Intensity: ");
  Serial.println(light);

  Serial.print("Pump Status: ");
  Serial.println(pumpStatus);

  if (alertMessage.length() > 0) {
    Serial.print("Alerts: ");
    Serial.println(alertMessage);
  }

  Serial.println("===============================");

  delay(5000);
}