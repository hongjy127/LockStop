import threading
import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer
import pigpio
import paho.mqtt.client as mqtt
from keypad import Keypad
from threading import Timer, Thread
from video import Video
from gpiozero import Button
import socket
import net
import cv2

client = mqtt.Client()
GPIO.setwarnings(False)

bz = Buzzer(16)
SERVO = 24

pi = pigpio.pi()
pi.set_servo_pulsewidth(SERVO, 700)  # 초기 0도

# 주소
# IP_ADDRESS = "172.30.1.39"  # 정연 pc
# IP_ADDRESS = "192.168.0.4"  # 해준 pc
IP_ADDRESS = "172.30.1.67"
# cmd로 sub 확인
# mosquitto_sub -v -h localhost -t iot/#
HOST = '172.30.1.67'  # 강의장

PORT = 5000

button = Button(20)



def publish(topic, value):
    try:
        client.connect(IP_ADDRESS)
        client.publish(topic, value)
        client.loop(2)
        print(topic, value)
    except Exception as e:
        print(f"에러 {e}")


def to_jpg(frame, quality=60):  # (변환할 이미지)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    is_success, jpg = cv2.imencode(".jpg", frame, encode_param)
    return jpg


def picture():
    save = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        writer = s.makefile('wb')
        # reader = s.makefile('rb')

        # image 획득해서 전송해줘야 함

        # cap = cv2.VideoCapture(1)
        ret, image = cap.read()
        if not ret:
            print('실패-----------------------------')
            return
        image = to_jpg(image)

        if (door == "right" or "wrong"):
            save = 1
        else:
            save = 0

        net.send(writer, image, save)

        cap.release()
        # cv2.destroyAllWindows()


if __name__ == '__main__':

    kp = Keypad()

    PASSWORD = "1234"
    confirm = ""  # 비밀번호와 일치시키는 확인 변수
    b_press = False
    counter = 0  # 비밀번호 3회오류시 noti 발생확인을 위한 변수
    timeout = 3  # 3초후에 리셋 함수 부르기 위해 만듬
    door = ""

    def reset():
        global confirm
        global b_press
        print('Time is up!')
        confirm = ""
        b_press = False

    t = None

    
    

    while(True):
        
        key = kp.getKey()  # 눌려진 key값을 받아옴
           
        if(key != None):
            bz.beep(0.1, n=1)  # 0.1초동안 한번 울림
            if(str(key) != "*"):  # 키입력중
                if(b_press == False):  # 첫번째 키 입력이면
                    #start = time.time()
                    b_press = True
                    # 3초동안 누르지 않을경우 settimeout 함수 구현해야 됨
                    t = Timer(timeout, reset)
                    t.start()

                else:
                    # pass #타이머 리스타트
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
                if(confirm[0] == "C"):  # 비밀번호 변경구간
                    PASSWORD = confirm[1:]
                    print("new password", PASSWORD)
                elif(confirm == PASSWORD):  # 비밀번호 맞으경우
                    cap = cv2.VideoCapture(0)
                    time.sleep(0.6)
                    counter = 0
                    door = "right"
                    print(door)
                    publish("iot/doorlock", "open")  # 앱에 open 이라고 알려줌
                    t1 = threading.Thread(target=picture)
                    t1.start()
                    pi.set_servo_pulsewidth(SERVO, 1500)  # 90도
                    time.sleep(3)
                    pi.set_servo_pulsewidth(SERVO, 700)  # 0도
                    door = ""
                    # cap.release()
                else:
                    cap = cv2.VideoCapture(0)
                    door ="wrong"
                    print(door)
                    time.sleep(0.6)
                    t1 = threading.Thread(target=picture)
                    t1.start()
                    bz.beep(2, n=1)
                    counter += 1
                    door = ""
                    # publish("iot/doorlock", "error1") # <-하이디에서 받는거
                    if (counter == 3):
                        counter = 0
                        publish("iot/doorlock", "error")  # <- 안드로이드 알림 받는거
                time.sleep(0.3)
                confirm = ""
                b_press = False
