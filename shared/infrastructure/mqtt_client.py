#Esto me dio copilot
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado con código de resultado " + str(rc))
    client.subscribe("tu/tema/iot")

client = mqtt.Client()
client.on_connect = on_connect

client.connect("broker.mqtt.com", 1883, 60)
client.loop_start()