import json
import os
import time
from pathlib import Path

import dotenv
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

DEVICE_ID = "mock_device"


def load_config() -> tuple[str, int, str]:

    dotenv.load_dotenv(Path(__file__).parent.parent / ".env")

    mqtt_host = os.getenv("MQTT_HOST")
    mqtt_port = os.getenv("MQTT_PORT")
    topic = os.getenv("MOCK_TOPIC")

    if not mqtt_host:
        raise ValueError("MQTT_HOST is not defined")

    if not mqtt_port:
        raise ValueError("MQTT_PORT is not defined")

    if not topic:
        raise ValueError("MOCK_TOPIC is not defined")

    return mqtt_host, int(mqtt_port), topic


def main():
    path = Path(__file__).parent.parent / ".env"

    print(path)

    mqtt_host, mqtt_port, topic = load_config()

    client = mqtt.Client(
        CallbackAPIVersion.VERSION2,
        client_id=DEVICE_ID,
    )

    client.connect(mqtt_host, mqtt_port)
    client.loop_start()

    try:
        while True:
            payload = json.dumps(
                {
                    "device_id": DEVICE_ID,
                    "value": "Rolling stones",
                    "timestamp": time.time(),
                }
            )

            result = client.publish(
                topic,
                payload,
                qos=1,
            )

            result.wait_for_publish()

            print(f"Published: {payload}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping sensor...")

    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
