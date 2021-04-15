from django.shortcuts import render
from django.views.generic import ListView, TemplateView
# Create your views here.






class RecordView(ListView):

    model = lockdata
    template_name = 'record.html'
    context_object_name = 'object_list' # 컨텍스트 객체 이름 변경(object_list)
    paginate_by = 10 # 페이지네이션, 페이지당 문서 건 수

class ConfigView(TemplateView):
    model = lockdata
    template_name = 'imageconfig.html'