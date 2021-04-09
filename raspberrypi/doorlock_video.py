# LED와 PIR 센서를 연결
# 움직임이 감지되면 동영상 녹화 시작, 서버로 이미지 전송
# 움직임이 없어지면 동영상 녹화 중지, 이미지 전송 중지
# 파일명은 날짜_녹화시작시간.h264
# 화면 출력은 없음

from gpiozero import Button
from signal import pause
from time import sleep
import picamera
import datetime
import socket
import struct
import threading
import io
import net

HOST = '172.30.1.39'
PORT = 5000

button = Button(21)

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.vflip = True

def video_streaming():
    save = 0
    with socket.socket() as s:
        s.connect((HOST, PORT))
        writer = s.makefile('wb')
        reader = s.makefile('rb')
        stream = io.BytesIO()

        # 동영상 -> 이미지
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                image = stream.getvalue()   # 스트림에서 byte 배열 얻기
                if button.is_pressed:
                    save = 1
                    print(save)
                else:
                    save = 0
                    print(save)
                
                net.send(writer, image, save)
                result = net.receive(reader)[0]

                # 다음 캡쳐를 위해 스트림을 리셋 - 파일의 기존 내용을 버림
                stream.seek(0)      # 파일 쓰기 위치를 맨 앞으로 이동
                stream.truncate()   # 기존 내용을 버리는 작업

                # if not button.value:
                #     writer.write(struct.pack('<L', 0))  # 스트리밍 끝
                #     writer.flush()
                #     break

def start_record():
    now = datetime.datetime.now()
    fname = now.strftime("%T%m%d_%H%M") + ".h264"
    camera.start_recording(fname)
    threading.Thread(target=video_streaming).start()

def stop_record():
    camera.stop_recording()

# def send_message():
#     print("press button")
    

while(1):
    start_record()
    # button.when_pressed=send_message
    # pause()