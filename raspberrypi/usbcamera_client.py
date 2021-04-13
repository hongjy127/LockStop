# USB camera
# Button 값을 save로 보냄
# image를 보냄

from video import Video
from gpiozero import Button
from time import sleep
import socket
import json
import net
import io
import cv2

# 주소
HOST = '172.30.1.39'
PORT = 5000

button = Button(21)

if __name__ == '__main__':
    save = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        writer = s.makefile('wb')
        reader = s.makefile('rb')
        # device 번호
        with Video(device=0) as v:
            for image in v:
                image = Video.to_jpg(image, 60)

                if button.is_pressed:
                    save = 1
                else:
                    save = 0

                net.send(writer, image,save)

                # result = net.receive(reader)[0]
                # print(json.loads(result.decode()))