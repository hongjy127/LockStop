from time import sleep
from signal import pause
import paho.mqtt.client as mqtt

client = mqtt.Client()
IP_ADDRESS = "172.30.1.39"  # pc
# cmd로 sub 확인
# mosquitto_sub -v -h localhost -t iot/#
def publish(topic, value):
    try:
        client.connect(IP_ADDRESS)
        client.publish(topic, value)
        client.loop(2)
        print(topic, value)
    except Exception as e:
        print(f"에러 {e}")

# publish("iot/doorlock", "open")

while(1):
    publish("iot/doorlock", "open")
    sleep(5)
    publish("iot/doorlock", "error")
    sleep(5)
    publish("iot/CJ", "full")
    sleep(5)
    publish("iot/CJ", "empty")
    sleep(5)
