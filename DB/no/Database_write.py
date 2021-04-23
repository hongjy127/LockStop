import paho.mqtt.client as mqtt
from mqtt_sub import subscribe
import MySQLdb
import datetime

client = mqtt.Client()
IP_ADDRESS_PC = "172.30.1.87"  # pc의 주소
IP_ADDRESS_PI = "172.30.1.15"  # raspberrypi 주소

db = MySQLdb.connect(host=IP_ADDRESS_PC, db="lockstop",user ="Lockstop",
                     passwd="1234",charset="utf8")

def data_upload(topic,value,fname): 
    query = f"""INSERT INTO lockdata(topic, value, image, date, time) 
            VALUES('{topic}', '{value}', '{fname}', CURDATE(), CURTIME())
            """
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()
    
    except Exception as e:
        print(f'에러 : {e}')

def publish(topic, value):
    try:
        client.connect(IP_ADDRESS_PI)
        client.publish(topic, value)
        client.loop(2)
        # print(topic, value)
    except Exception as e:
        print(f"에러 {e}")

def on_message(client, userdata, msg):
    now = datetime.datetime.now()
    fname = now.strftime("%y%m%d%H%M%S")
    filepath = f"C:/Users/hongj/LockStop/python/image/{fname}.jpeg"
    topic = msg.topic
    message = msg.payload.decode('utf-8')
    if topic == "iot/doorlock" or topic == "iot/CJ":
        data_upload(topic, message, filepath)
        publish("iot/photo", fname)
        # raspberry에서 iot/photo를 받은 경우 사진을 캡쳐하고 fname으로 저장
        print('memo complete')

subscribe('localhost', 'iot/#', on_message)
