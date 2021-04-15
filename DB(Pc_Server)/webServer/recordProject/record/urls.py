from record.views import RecordView, ConfigView
from django.contrib import admin
from django.urls import path
# from mjpeg.views import *

urlpatterns = [
    path('', RecordView.as_view(), name='record'),
    path('image/',ConfigView.as_view(), name='imageconfig'),
]