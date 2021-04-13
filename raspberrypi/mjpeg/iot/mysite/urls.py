from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mjpeg/', include('mjpeg.urls')),
    # path('kakao/', include('kakao.urls')),
    path('api/', include('api.urls')),
]
