from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse, StreamingHttpResponse, Http404
from mysite.picam import MJpegStreamCam
import time

mjpegstream = MJpegStreamCam()


from xxx import data


def stream_gen() :
    yield (b'--myboundary\n'
            b'Content-Type:image/jpeg\n'
            b'Content-Length: ' + f"{len(data)}".encode() + b'\n'
            b'\n' + data + b'\n')


class CamView(TemplateView):
    template_name = "cam.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode", "#")
        return context


def mjpeg_stream(request):
    return StreamingHttpResponse(stream_gen(),
                                 content_type='multipart/x-mixed-replace;boundary=--myboundary')


# return StreamingHttpResponse(mjpegstream,
#                                  content_type='multipart/x-mixed-replace;boundary=--myboundary')
