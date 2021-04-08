from time import sleep
import paho.mqtt.client as mqtt

client = mqtt.Client()
IP_ADDRESS = "192.168.0.4"  # pc

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
    publish("iot/CJ", "full")
    sleep(5)
    publish("iot/CJ", "empty")
    sleep(5)

