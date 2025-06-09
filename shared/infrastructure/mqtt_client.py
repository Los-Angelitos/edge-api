import paho.mqtt.client as mqtt
import os

class MQTTClient:
    def __init__(self):
        self.HOST = os.getenv('HOST_MQTT')
        self.PORT = int(os.getenv('PORT_MQTT', 1883))
        self.USERNAME = os.getenv('USERNAME_MQTT')
        self.PASSWORD = os.getenv('PASSWORD_MQTT')

        self._client = mqtt.Client()
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._topics_to_subscribe = [
            "devices/termostats"
        ]

        self._client.username_pw_set(self.USERNAME, self.PASSWORD)
        self._client.connect(self.HOST, self.PORT, 60)
        self.subscribe_topics()
        print(f"MQTT client initialized with host: {self.HOST}, port: {self.PORT}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker successfully")
        else:
            print(f"Failed to connect, return code {rc}")
            
    def on_message(self, client, userdata, msg):
        print(f"Message received: {msg.topic} {msg.payload.decode()}")

    def subscribe_topics(self):
        for topic in self._topics_to_subscribe:
            self._client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")

    def publish(self, topic, payload):
        self._client.publish(topic, payload)
        print(f"Published to topic: {topic} with payload: {payload}")
    
    def loop_start(self):
        self._client.loop_forever()
        print("MQTT client loop started")