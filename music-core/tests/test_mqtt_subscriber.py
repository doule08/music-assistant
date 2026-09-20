import json
from typing import Any
from unittest.mock import Mock

import paho.mqtt.client as mqtt

from config.settings import settings
from infrastructure.mqtt.mqtt_subscriber import MqttSubscriber


class FakeMQTTMessage(mqtt.MQTTMessage):
    def __init__(self, topic: str, payload: bytes):
        super().__init__(mid=0, topic=topic.encode("utf-8"))
        self.payload = payload


def make_message(topic: str, payload: dict[str, Any]) -> FakeMQTTMessage:
    return FakeMQTTMessage(topic, json.dumps(payload).encode("utf-8"))


def test_mqtt_subscriber_on_connect_subscribes_to_configured_topic():
    subscriber = MqttSubscriber(host="localhost", port=1883)
    client = Mock()

    subscriber.on_connect(client, None, None, 0, None)

    client.subscribe.assert_called_once_with(settings.mock_topic, qos=1)


def test_mqtt_subscriber_start_connects_and_starts_loop_once():
    subscriber = MqttSubscriber(host="localhost", port=1883)
    subscriber.client.connect = Mock()
    subscriber.client.loop_start = Mock()

    subscriber.start()
    subscriber.start()

    subscriber.client.connect.assert_called_once_with("localhost", 1883)
    subscriber.client.loop_start.assert_called_once()


def test_mqtt_subscriber_on_message_decodes_json_and_dispatches():
    subscriber = MqttSubscriber(host="localhost", port=1883)
    subscriber.handle_message = Mock()
    payload = {"value": 42, "timestamp": "abc"}

    subscriber.on_message(Mock(), None, make_message(settings.mock_topic, payload))

    subscriber.handle_message.assert_called_once_with(settings.mock_topic, payload)


def test_mqtt_subscriber_invalid_json_is_ignored():
    subscriber = MqttSubscriber(host="localhost", port=1883)
    subscriber.handle_message = Mock()
    message = FakeMQTTMessage(settings.mock_topic, b"{not valid json}")

    subscriber.on_message(Mock(), None, message)

    subscriber.handle_message.assert_not_called()


def test_mqtt_subscriber_handle_message_prints_value_for_matching_topic(capsys):
    subscriber = MqttSubscriber(host="localhost", port=1883)
    payload = {"value": 27, "timestamp": "123"}

    subscriber.handle_message(settings.mock_topic, payload)

    captured = capsys.readouterr()
    assert "123" in captured.out
    assert "27 value" in captured.out
