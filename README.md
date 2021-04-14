# 실행순서



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





## Android

- 앱실행