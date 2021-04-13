from django.shortcuts import render
from django.http import JsonResponse
from gpiozero import Buzzer
# import pigpio
import time

buzzer = Buzzer(16)

def buzzercontrol(request):
    # target = request.GET["target"]    # 키가 없으면 예외 발생
    target = request.GET.get("target")  # 키가 없으면 None 리턴
    value = request.GET.get("value", "off") # 키가 없으면 2번째 인자 리턴
    
    if target == "1":
        if value == "on":
            for i in range(50):
                buzzer.on()
                time.sleep(0.1)
                buzzer.off()
                time.sleep(0.1)

        elif value == "off":
            buzzer.off()

    result = {
        "result": "OK",
        "target": target,
        "value": value
    }

    return JsonResponse(result)