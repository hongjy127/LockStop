import net
import json
import cv2
import numpy as np

HOST = '172.30.1.39'    # 내 pc의 주소
PORT = 5000
counter = 0

def show_image(data, frame_name):
    # byte 배열을 numpy로 변환
    data = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # Video.show()
    cv2.imshow(frame_name, image)   # 스레드별로 frame이름이 달라야함
    cv2.waitKey(1)  # 이미지 갱신이 일어나는 곳

def receiver(client, addr):
    global counter
    counter += 1
    frame_name = f'frame {counter}'

    reader = client.makefile('rb')
    writer = client.makefile('wb')
    while True:
        data, data_len = net.receive(reader)
        if not data:
            break
        # print('received ', data_len)    # 이미지 처리
        # AI 알고리즘 처리
        show_image(data, frame_name)
        result = json.dumps({'result':'ok'})
        net.send(writer, result.encode())
    print('exit receiver')

if __name__=='__main__':
    print('start server...')
    net.server(HOST, PORT, receiver)