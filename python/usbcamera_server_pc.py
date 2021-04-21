import net
import json
import cv2
import numpy as np
import datetime
import sys

# 주소
# HOST = '192.168.0.4'    # 내 pc의 주소
HOST = '172.30.1.67'
# HOST = '172.30.1.39'
# HOST = '192.168.0.36' # 태석pc

PORT = 5000
counter = 0

def show_image(data, frame_name):
    # byte 배열을 numpy로 변환
    data = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    key = cv2.waitKey(1)  # 이미지 갱신이 일어나는 곳
    return (image, key)

def receiver(client, addr):
    global counter
    counter += 1
    frame_name = f'frame {counter}'

    reader = client.makefile('rb')
    # writer = client.makefile('wb')


    data, data_len, save = net.receive(reader)
    print('-------수신 ', data_len)        
    if not data_len : return
    # data : jpeg 이미지
    # image : bgr 이미지
    image, key = show_image(data, frame_name)
    # AI 알고리즘 처리
    
    if save == 1:
        now = datetime.datetime.now()
        fname = now.strftime("%y%m%d%H%M%S") + ".jpeg"
        # 파일 경로
        filename = "C:/Users/wjdgo/iot_project/LockStop/python/image/"+fname
        # filename = "C:/Users/hongj/LockStop/python/image/"+fname
        cv2.imwrite(filename, image)

        # result = json.dumps({'result':'ok'})
        # net.send(writer, result.encode())
    
    cv2.destroyAllWindows()
    print('exit receiver')

if __name__=='__main__':
    print('start server...')
    net.server(HOST, PORT, receiver)