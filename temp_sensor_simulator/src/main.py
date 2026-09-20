import json
import random
import time

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import dotenv
import os
from pathlib import Path

dotenv.load_dotenv(Path(__file__).parent.parent.parent / ".env")

MQTT_HOST = str(os.getenv("MQTT_HOST"))
MQTT_PORT = int(str(os.getenv("MQTT_PORT")))
TOPIC = "music/sensor/mock"
DEVICE_ID = "mock_device"

# create client
client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id=DEVICE_ID)

# connect
client.connect(
    MQTT_HOST,
    MQTT_PORT,
)

# start loop
client.loop_start()


# sending loop
try:
    while True:
        payload = json.dumps(
            {
                "device_id": f"d",
                "value": random.randrange(1, 100, 1),
                "timestamp": time.time(),
            }
        )

        result = client.publish(TOPIC, payload, qos=1)

        result.wait_for_publish()

        print(f"Published : {payload}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping sensor...")

finally:
    client.loop_stop()
    client.disconnect()
