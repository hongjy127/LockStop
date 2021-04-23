import net
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from mqtt_sub import subscribe
import MySQLdb
import threading


# 주소
# HOST = '192.168.0.4'    # 내 pc의 주소
IP_ADDRESS_PC = '172.30.1.87'
IP_ADDRESS_PI = "172.30.1.15"  # raspberrypi 주소
# HOST = '172.30.1.39'
# HOST = '192.168.0.36' # 태석pc
PORT = 5000

client = mqtt.Client()
db = MySQLdb.connect(host=IP_ADDRESS_PC, db="lockstop",user ="Lockstop",
                     passwd="1234",charset="utf8")
counter = 0
num = 0

def sub():
    subscribe('localhost', 'iot/#', on_message)

def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode('utf-8')

    if topic == "iot/doorlock" or topic == "iot/CJ":
        data_upload(topic, message)
        # publish("iot/photo", fname)
        # raspberry에서 iot/photo를 받은 경우 사진을 캡쳐하고 fname으로 저장
        print('memo complete')

def show_image(data, frame_name):
    # byte 배열을 numpy로 변환
    data = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    key = cv2.waitKey(1)  # 이미지 갱신이 일어나는 곳
    return (image, key)

def receiver(client, addr):
    global num
    global counter
    counter += 1
    frame_name = f'frame {counter}'

    reader = client.makefile('rb')
    # writer = client.makefile('wb')

    data, data_len, fname, save = net.receive(reader)
    print('-------수신 ')       
     
    if not data_len : return
    # data : jpeg 이미지
    # image : bgr 이미지
    image, key = show_image(data, frame_name)
    # AI 알고리즘 처리
    
    if save == 1:
        # now = datetime.datetime.now()
        # fname = now.strftime("%y%m%d%H%M%S") + ".jpeg"
        # 파일 경로
        fname = fname.decode()
        print(fname)
        filepath = "C:/Users/hongj/LockStop/python/image/"+fname+".jpeg"
        print(filepath)
        # filename = "C:/Users/hongj/LockStop/python/image/"+fname
        cv2.imwrite(filepath, image)
        data_update(filepath)

        # result = json.dumps({'result':'ok'})
        # net.send(writer, result.encode())
    
    cv2.destroyAllWindows()
    print('exit receiver')

def data_upload(topic,value): 
    global num
    query = f"""INSERT INTO lockdata(topic, value, date, time, num) 
            VALUES('{topic}', '{value}', CURDATE(), CURTIME(), '{num}')
            """
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()
    
    except Exception as e:
        print(f'에러 : {e}')

def data_update(fname):
    global num
    query = f"""UPDATE lockdata
            SET image='{fname}'
            WHERE num = '{num}'
            """
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()
    
    except Exception as e:
        print(f'에러 : {e}')

    num += 1

def publish(topic, value):
    try:
        client.connect(IP_ADDRESS_PI)
        client.publish(topic, value)
        client.loop(2)
        # print(topic, value)
    except Exception as e:
        print(f"에러 {e}")





if __name__=='__main__':
    t=threading.Thread(target=sub)
    t.start()
    net.server(IP_ADDRESS_PC, PORT, receiver)
    print('start server...')

    