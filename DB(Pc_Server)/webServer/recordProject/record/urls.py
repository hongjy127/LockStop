from record.views import TestLV, TestDV
from django.contrib import admin
from django.urls import path
# from mjpeg.views import *

urlpatterns = [
    path('', TestLV.as_view(), name='record'),
    path('image/<int:pk>',TestDV.as_view(), name='detail'),

]