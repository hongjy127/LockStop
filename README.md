# 실행순서



## IP 주소

- PC
  - usbcamera_server.py > HOST(pc주소), FILEPATH
- Android
  - MainActivity.kt > SERVER_URI(pc주소)
  - MainActivity.kt > doorLockView.loadUrl(pi주소)
  - PiApiService.kt > BASE_URL(pi주소)
- raspberrypi
  - mjpeg/iot/mysite/settings.py > ALLOWED_HOSTS
  - (임시) keypad_client.py > IP_ADDRESS(pc주소)
  - (임시) noti_test_pub.py > IP_ADDRESS(pc주소)





## Raspberrypi

- 서버 실행

```
// 경로에서(mjpeg)
$ python manage.py runserver 0.0.0.0:8000
```

- noti_test_pub.py (마그네틱 센서, 도어락 임시)

```
$ python noti_test_pub.py

// 도어락
$ sudo pigpiod
$ python keypad.py
```

- usbcamera_client.py

```
// PC 서버 기동 후
$ python usbcamera_client.py
```



## PC

- usbcamera_server.py

```
$ python usbcamera_server.py
```

- (임시) arduino 가변저항 연결 -> 로드셀로 변경

-  pc DB 설정

  - IP_ADDRESS = "Pc주소"

    db = MySQLdb.connect(host="Pc주소", db="lockstop",user ="root권장",

    ​           passwd="비밀번호",charset="utf8")



## Android

- arduino\pub_loadcell\mag\app.ino 실행