from keypad import Keypad
import time
from gpiozero import Buzzer
import pigpio
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from threading import Thread, Event, Timer


client = mqtt.Client()
GPIO.setwarnings(False)

bz = Buzzer(16)
SERVO = 24


pi = pigpio.pi()
pi.set_servo_pulsewidth(SERVO, 700)  # 초기 0도

# 주소
# IP_ADDRESS = "172.30.1.39"  # 정연 pc
IP_ADDRESS = "192.168.0.4"  # 해준 pc
# IP_ADDRESS = "192.168.0.36"  # 태석 pc
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



if __name__ == '__main__':
    kp = Keypad()

    PASSWORD = "1234"
    confirm = ""
    b_press = False
    counter = 0
    timeout = 5

    def reset():
        global confirm
        global b_press
        print('Time is up!')
        confirm = ""
        b_press = False


    while(True):
        key = kp.getKey()
        if(key != None):
            bz.beep(0.1, n=1)
            if(str(key) != "*"):  # 키입력중
                if(b_press == False):  # 첫번째 키 입력이면
                    t = Timer(timeout, reset)
                    t.start()
                    b_press = True
                    # 3초동안 누르지 않을경우 settimeout 함수 구현해야됨
                else:
                    t.cancel()
                    t = Timer(timeout, reset)
                    t.start()
                time.sleep(0.3)
                print(key)
                confirm += str(key)
            else:
                t.cancel()
                print(input)
                # 'C'로 시작하면 새로운 비밀번호 저장
                # 'C0248'이면 '0248'이 새로운 비밀번호가 됨
                print(confirm)
                if(confirm[0] == "C"):
                    PASSWORD = confirm[1:]
                    print("new password", PASSWORD)
                elif(confirm == PASSWORD):
                    counter = 0
                    print("right")
                    publish("iot/doorlock", "open")
                    pi.set_servo_pulsewidth(SERVO, 1500)  # 90도
                    time.sleep(3)
                    pi.set_servo_pulsewidth(SERVO, 700)  # 0도
                else:
                    print("wrong")
                    bz.beep(2, n=1)
                    counter += 1
                    publish("iot/doorlock", "error1")  # <-하이디에서 받는거
                    if (counter == 3):
                        counter = 0
                        publish("iot/doorlock", "error")  # <- 안드로이드 알림 받는거

                time.sleep(0.3)
                confirm = ""
                b_press = False
