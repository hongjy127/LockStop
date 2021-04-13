from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    # path('led/', ledcontrol),        # /api/led?target=1&value=on
    # path('servo/', servocontrol)    # /api/servo?target=1&value=35
    path('buzzer/', buzzercontrol)      # /api/buzzer?target=1&value=on
]