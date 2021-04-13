from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse, StreamingHttpResponse, Http404
from mysite.picam import MJpegStreamCam
from time import sleep

mjpegstream = MJpegStreamCam(width=320, height=240)
class CamView(TemplateView):
    template_name = "cam.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode", "#")
        return context

def snapshot(request):
    sleep(0.2)
    image = mjpegstream.snapshot()
    return HttpResponse(image, content_type="image/jpeg")

def mjpeg_stream(request):
    return StreamingHttpResponse(mjpegstream,
            content_type='multipart/x-mixed-replace;boundary=--myboundary')
            