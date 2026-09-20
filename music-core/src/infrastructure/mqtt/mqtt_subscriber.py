import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from config.settings import settings


class MqttSubscriber:
    CLIENT_ID = "music-core"
    TOPIC = settings.mock_topic

    def __init__(self, host=settings.mqtt_host, port=settings.mqtt_port) -> None:
        self.host = host
        self.port = port

        self.client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=self.CLIENT_ID)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self):
        self.client.connect(self.host, self.port)
        print("Connecting to MQTT broker...")
        self.client.loop_forever()

    def on_connect(self, client: mqtt.Client, userdata, flags, reason_code):
        # reason_code = ??
        print(f"Connected to MQTT broker : {reason_code}")
        client.subscribe(self.TOPIC, qos=1)

    def on_message(self, client, userdata, message: mqtt.MQTTMessage):
        try:
            payload = json.loads(message.payload.decode("utf-8"))

            print(f"Topic : {message.topic}")
            print(f"Data : {payload}")

            self.handle_message(message.topic, payload)
        except json.JSONDecodeError:
            print(f"Invalid JSON received on {message.topic}")

    def handle_message(self, topic, payload):
        if topic == self.TOPIC:
            value = payload.get("value")
            timestamp = payload.get("timestamp")

            print(f"{timestamp} : {value} value")
