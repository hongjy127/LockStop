from record.views import CJ, DoorLock, TestLV, TestDV,LockstopYAV, LockstopMAV, TodayDAV,ChangedayDAV
from django.contrib import admin
from django.urls import path
# from mjpeg.views import *

urlpatterns = [
    path('', TestLV.as_view(), name='record'),
    path('image/<int:pk>',TestDV.as_view(), name='detail'),

    # 필터를 위한 url
    path('doorlock/', DoorLock.as_view(), name='doorlock'),
    path('CJ/', CJ.as_view(), name='CJ'),
    
    # 날짜별로 보기위한 
    path('archive/', TodayDAV.as_view(), name='today'),
    path('archive/<int:year>/<int:month>/<int:day>/', ChangedayDAV.as_view(), name='change_day'),
   

]