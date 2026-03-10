# comms/mqtt_client.py
import json
import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker="localhost", port=1883, intersection_id="A"):
        self.broker = broker
        self.port = port
        self.intersection_id = intersection_id
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def publish_state(self, snapshot):
        topic = f"intersection/{self.intersection_id}/state"
        payload = json.dumps(snapshot)
        self.client.publish(topic, payload)

    def subscribe_neighbors(self, on_message_cb):
        def _on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())
                on_message_cb(msg.topic, data)
            except Exception as e:
                print("MQTT decode error:", e)

        self.client.on_message = _on_message
        self.client.subscribe("intersection/+/state")
