from time import sleep
import time
from signal import pause
import paho.mqtt.client as mqtt
import sqlite3
import MySQLdb
import datetime


client = mqtt.Client()
IP_ADDRESS = "172.30.1.69"  # pc의 주소

db = MySQLdb.connect(host="172.30.1.69", db="lockstop",user ="Lockstop",
                     passwd="1234",charset="utf8")


def publish(topic,value,filepath):
    # today = time.ctime()
    

    query = f"""INSERT INTO lockdata(topic, value, image, date, time) 
            VALUES('{topic}','{value}','{filepath}',CURDATE(), CURTIME())
            """
    try:
        client.connect(IP_ADDRESS)
        client.publish(topic,value)

        cursor = db.cursor()
        cursor.execute(query)

        db.commit()

        cursor.close()
        # db.close()

        client.loop(2)
    
    except Exception as e:
        print(f'에러 : {e}')
    

while(1):
    now = datetime.datetime.now()
    fname = now.strftime("%y%m%d%H%M%S") + ".jpeg"
    filepath = f"C:/Users/rjh76\LockStop\python\image/{fname}"

    publish('iot/doorlock',"open",filepath)
    print('memo complete')
    sleep(5)

    # publish('iot/doorlock','error',filepath)
    # print('memo complete')
    # sleep(5)

    # publish('iot/CJ',"full",filepath)
    # print('memo complete')
    # sleep(5)
    
    # publish('iot/CJ','empty',filepath)
    # print('memo complete')
    # sleep(5)