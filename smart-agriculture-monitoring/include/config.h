#ifndef CONFIG_H
#define CONFIG_H

// ===== SENSOR PINS =====

#define DHT_PIN 4

#define SOIL_PIN 34
#define WATER_PIN 32
#define LDR_PIN 35

#define RELAY_PIN 26

// ===== MQTT =====

const char *MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;

const char *TOPIC_SENSOR = "smartfarm/sensors";
const char *TOPIC_ALERTS = "smartfarm/alerts";
const char *TOPIC_PUMP = "smartfarm/pump";

#endif