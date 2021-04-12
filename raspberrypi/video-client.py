from video import Video
from gpiozero import Button
from time import sleep
import socket
import json
import net
import io
import cv2


HOST = '192.168.0.4'
PORT = 5000

button = Button(20)

if __name__ == '__main__':
    save = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        writer = s.makefile('wb')
        reader = s.makefile('rb')
        with Video(device=1) as v:
            for image in v:
                image = Video.to_jpg(image, 60)

                if button.is_pressed:
                    save = 1
                    # print(save)
                else:
                    save = 0
                    # print(save)

                # print('video send ', len(image))
                net.send(writer, image,save)

                # result = net.receive(reader)[0]
                # print(json.loads(result.decode()))