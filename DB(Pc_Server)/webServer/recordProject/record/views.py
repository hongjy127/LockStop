from record.models import Lockdata
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
# Create your views here.





# ListView
class TestLV(ListView):
    model = Lockdata
    template_name = 'record/record.html' # 템플릿 파일명 변경
    # context_object_name = 'object_list' # 컨텍스트 객체 이름 변경(object_list)
    # paginate_by = 10 # 페이지네이션, 페이지당 문서 건 수

    # def get_context_data(self,**kwargs):  
    #     context = super().get_context_data(**kwargs)
    #     context['object_list'] = Lockdata.objects.all()
        
    #     return context


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
