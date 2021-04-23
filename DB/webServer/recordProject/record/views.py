from typing import List

from django.views.generic.base import TemplateView
from record.models import Lockdata
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from django.views.generic.dates import YearArchiveView, MonthArchiveView, TodayArchiveView, DayArchiveView

from datetime import datetime, timedelta


# ListView
class TestLV(ListView):
    model = Lockdata
    template_name = 'record/record.html' # 템플릿 파일명 변경
    context_object_name = 'object_list' # 컨텍스트 객체 이름 변경(object_list)
    
    paginate_by = 5 # 페이지네이션, 페이지당 문서 건 수
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Lockdata.objects.all().order_by('-id')
        return context
    

    # def get_context_data(self,**kwargs):  
    #     context = super().get_context_data(**kwargs)
    #     context['object_list'] = Lockdata.objects.all()
    #     return context

    # lockdata = Lockdata.objects.all()
    # Lockdata.objects.create(topic='토픽',value='값')
    # Lockdata.objects.filter(topic__contains="doorlock")

class DoorLock(ListView):
    model = Lockdata
    template_name = 'record/doorlock.html'
    paginate_by = 5
    # doorlock_data = Lockdata.objects.filter(topic__contains="doorlock")
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Lockdata.objects.filter(topic__contains="doorlock").order_by('-id')

        return context


class CJ(ListView):
    model = Lockdata
    template_name = 'record/CJ.html'
    paginate_by = 5 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Lockdata.objects.filter(topic__contains="CJ").order_by('-id')

        return context

class DateList(ListView):
    model = Lockdata
    template_name ='record/datelist.html'
    paginate_by = 5
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Lockdata.objects.filter(date__contains="2")

        return context


class TestDV(DetailView):
    model = Lockdata
    template_name = 'record/imageconfig.html'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['object_list'] = Lockdata.objects.()
        
    #     return context
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        obj =context["object"]
        # obj = self.get_object()
        # print(obj)
        context["imgdata"] = obj.image.split("/")[-1]


        return context
            

    # context_object_name = 'object_list'

class LockstopYAV(YearArchiveView):
    model= Lockdata
    date_field = 'date'
    make_object_list = True
class LockstopMAV(MonthArchiveView):
    model= Lockdata
    date_field = 'date'
    month_format = '%m'



class TodayDAV(TodayArchiveView):
    model= Lockdata
    date_field = 'date'
    month_format = '%m'
    template_name = 'record/todaylist.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class ChangedayDAV(DayArchiveView):
    model= Lockdata
    allow_empty=True
    date_field = 'date'
    month_format = '%m'
    template_name = 'record/changedaylist.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context['next_day'])
        return context

        


# class LockstopDAV(ListView):
#     model= Lockdata
#     # date_field = 'date'
#     # month_format = '%m'
#     template_name = 'record/datelist.html'
