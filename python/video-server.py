import net
import json
import cv2
import numpy as np
import datetime
import sys

HOST = '172.30.1.39'    # 내 pc의 주소
PORT = 5000
counter = 0

def show_image(data, frame_name):
    # byte 배열을 numpy로 변환
    data = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # Video.show()
    cv2.imshow(frame_name, image)   # 스레드별로 frame이름이 달라야함
    key = cv2.waitKey(1)  # 이미지 갱신이 일어나는 곳
    return (image, key)

def receiver(client, addr):
    global counter
    counter += 1
    frame_name = f'frame {counter}'

    reader = client.makefile('rb')
    writer = client.makefile('wb')
    # out = cv2.VideoWriter(filename, fourcc, 20, (640, 480), isColor=True)

    while True:
        data, data_len, save = net.receive(reader)
        # print(sys.getsizeof(data))
        # print(data_len)
        # print(save)
        if not data:
            break
        # data : jpeg 이미지
        image, key = show_image(data, frame_name)
        # print(image.shape)
        # image : bgr 이미지
        # out.write(image)
        # print('received ', data_len)    # 이미지 처리
        # AI 알고리즘 처리
        
        if save == 1:
            now = datetime.datetime.now()
            fname = now.strftime("%y%m%d%H%M%S") + ".jpeg"
            # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            filename = "C:/Users/hongj/LockStop/python/image/"+fname
            # print(filename)
            # print('capture')
            cv2.imwrite(filename, image)
            # print('ok')


        # result = json.dumps({'result':'ok'})
        # net.send(writer, result.encode())
    
    
    # out.release()
    cv2.destroyAllWindows()
    print('exit receiver')

if __name__=='__main__':
    print('start server...')
    net.server(HOST, PORT, receiver)