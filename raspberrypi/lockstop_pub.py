from time import sleep
from signal import pause
import paho.mqtt.client as mqtt

client = mqtt.Client()
IP_ADDRESS = "172.30.1.39"  # pc

def publish(topic, value):
    try:
        client.connect(IP_ADDRESS)
        client.publish(topic, value)
        client.loop(2)
    except Exception as e:
        print(f"에러 {e}")

while(1):
    publish("iot/doorlock", "open")
    sleep(5)
    publish("iot/doorlock", "error")
    sleep(5)
