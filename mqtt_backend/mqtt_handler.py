import json
import paho.mqtt.client as mqtt
import config
from logger import system_logger

class MQTTClientHandler:
    def __init__(self, message_callback=None):
        """
        Central MQTT connection handler.
        message_callback: function to call when a message arrives. Signature: callback(topic, payload_dict)
        """
        # Specify CallbackAPIVersion.VERSION2 for paho-mqtt 2.x
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.message_callback = message_callback
        self.connected_before = False

        # Setup standard callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        # Configure automatic reconnect delays
        self.client.reconnect_delay_set(config.RECONNECT_DELAY_MIN, config.RECONNECT_DELAY_MAX)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        """
        Callback triggered when client connects to the broker.
        """
        from system_health import update_system_health
        if reason_code == 0:
            system_logger.info("Successfully connected to MQTT Broker.")
            if self.connected_before:
                from event_logger import log_event
                log_event("MQTT Reconnected")
            else:
                self.connected_before = True
            
            update_system_health("CONNECTED")
            
            # Subscribe to the configured topics
            self.subscribe(config.TOPIC_SENSOR)
            self.subscribe(config.TOPIC_ALERTS)
            self.subscribe(config.TOPIC_PUMP)
        else:
            system_logger.error(f"MQTT Connection failed with Reason Code: {reason_code}")
            update_system_health("DISCONNECTED")

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        """
        Callback triggered when client disconnects. Reconnect is handled automatically.
        """
        system_logger.warning(f"MQTT Client disconnected (Reason Code: {reason_code}). Retrying automatically in background...")
        from system_health import update_system_health
        update_system_health("DISCONNECTED")

    def _on_message(self, client, userdata, msg):
        """
        Callback triggered when a published message is received.
        Parses JSON payload and routes to the subscriber processing pipeline.
        """
        topic = msg.topic
        payload_str = msg.payload.decode("utf-8", errors="ignore")

        # Ignore empty keepalives/payloads
        if not payload_str.strip():
            return

        if topic == config.TOPIC_SENSOR:
            try:
                payload_data = json.loads(payload_str)
            except json.JSONDecodeError as e:
                system_logger.error(f"Failed to parse JSON payload on sensor topic '{topic}': {e}. Payload: {payload_str}")
                return
        else:
            # Try to parse as JSON for other topics, fall back to plain string on failure
            try:
                payload_data = json.loads(payload_str)
            except json.JSONDecodeError:
                payload_data = payload_str

        # Forward the data to the subscriber callback
        if self.message_callback:
            try:
                self.message_callback(topic, payload_data)
            except Exception as e:
                system_logger.error(f"Error in message callback logic for topic '{topic}': {e}", exc_info=True)

    def connect(self):
        """
        Establishes connection to the broker.
        """
        system_logger.info(f"Connecting to MQTT Broker at {config.BROKER}:{config.PORT}...")
        try:
            self.client.connect(config.BROKER, config.PORT, config.KEEPALIVE)
        except Exception as e:
            system_logger.error(f"Initial broker connection failed: {e}")
            raise e

    def subscribe(self, topic: str):
        """
        Subscribes to a topic. Can be used for future topic expansion.
        """
        self.client.subscribe(topic)
        system_logger.info(f"Subscribed to topic: {topic}")

    def start(self):
        """
        Starts the non-blocking background loop network thread.
        """
        self.client.loop_start()
        system_logger.info("MQTT background network loop started.")

    def stop(self):
        """
        Stops the loop thread and disconnects gracefully.
        """
        self.client.loop_stop()
        self.client.disconnect()
        system_logger.info("MQTT Client disconnected gracefully.")
