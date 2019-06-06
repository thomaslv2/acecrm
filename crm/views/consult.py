from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from django.views import View
from django.db.models import Q
from crm.utils.pagination import Pagination
from django.http.request import QueryDict
from crm.utils.urls import reverse_url
from crm.forms import ConsultForm
from django.conf import settings

class ConsultList(View):
    def get(self,request,customer_id):
        q=self.search([])
        # print(request.current_menu_id)
        # print(request.session.get(settings.MENU_SESSION_KEY))
        if customer_id=='0':
            all_consult = models.ConsultRecord.objects.filter(q,delete_status=False,consultant=request.user_obj).order_by('-date')
        else:
            all_consult = models.ConsultRecord.objects.filter(q,delete_status=False,customer_id=customer_id,consultant=request.user_obj).order_by('-date')
        page = Pagination(request.GET.get('page'), all_consult.count(),request.GET.copy(), per_num=10)
        return render(request, 'consultant/consult_list.html', {'all_consult': all_consult[page.start:page.end], 'page_html':page.page_html})

    def post(self,request,customer_id):
        action=request.POST.get('action')
        if not hasattr(self,action):
            return HttpResponse('非法操作')
        else:
            getattr(self,action)()
        return self.get(request,customer_id)

    def search(self,fieldlist):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q=Q()
        q.connector='OR'
        for field in fieldlist:
            q.children.append(Q(('{}__contains'.format(field),query)))
        return q

def add_consult(request):
    obj=models.ConsultRecord(consultant=request.user_obj)
    form_obj=ConsultForm(instance=obj)
    if request.method=='POST':
        form_obj=ConsultForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse_url(request,'consult_list'))
    return render(request, 'consultant/add_consult.html', {'form_obj':form_obj})

def edit_consult(request,edit_id):
    obj=models.ConsultRecord.objects.filter(pk=edit_id).first()
    form_obj=ConsultForm(instance=obj)
    if request.method=='POST':
        form_obj=ConsultForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse_url(request,'consult_list'))
    return render(request, 'consultant/edit_consult.html', {'form_obj':form_obj})
