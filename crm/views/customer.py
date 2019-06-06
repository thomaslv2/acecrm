from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.forms import CustomerForm
from django.views import View
from django.db.models import Q
from crm.utils.pagination import Pagination
from django.http.request import QueryDict
from crm.utils.urls import reverse_url
from django.db import transaction
from ace_crm.settings import MAX_CUSTOMER_NUM


# def customer_list(request):
#     #公户展示
#     if request.path_info==reverse('customer_list'):
#         all_customer = models.Customer.objects.filter(consultant__isnull=True)
#     else:
#         all_customer = models.Customer.objects.filter(consultant=request.user_obj)
#     return render(request, 'customer_list.html',  {'all_customer': all_customer})

class CustomerList(View):

    def get(self,request):

        q=self.search(['qq','name'])
        # 公户展示
        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q,consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q,consultant=request.user_obj)
        page = Pagination(request.GET.get('page'), all_customer.count(),request.GET.copy(), per_num=10)
        return render(request, 'consultant/customer_list.html', {'all_customer': all_customer[page.start:page.end], 'page_html':page.page_html})

    def post(self,request):
        action=request.POST.get('action')
        if not hasattr(self,action):
            return HttpResponse('非法操作')
        else:
            ret=getattr(self,action)()
            if ret:
                return ret
        return self.get(request)
    
    def multi_apply(self):
        ids=self.request.POST.getlist('ids')
        #判断客户数量是否已达上限
        if self.request.user_obj.customers.all().count()+len(ids)>MAX_CUSTOMER_NUM:
            return HttpResponse('用户数量已达上限，请释放部分用户后再选择')

        with transaction.atomic():
            queryset=models.Customer.objects.filter(pk__in=ids,consultant__isnull=True).select_for_update()
            if len(ids)==queryset.count():
                queryset.update(consultant=self.request.user_obj)
                return
            return HttpResponse('数据已改动，请重新选取！')
        # self.request.user_obj.customers.add(*models.Customer.objects.filter(pk__in=ids))

    def multi_pub(self):
        ids = self.request.POST.getlist('ids')
        models.Customer.objects.filter(pk__in=ids).update(consultant=None)

    def search(self,fieldlist):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q=Q()
        q.connector='OR'
        for field in fieldlist:
            q.children.append(Q(('{}__contains'.format(field),query)))
        return q

def add_customer(request):
    form_obj=CustomerForm()
    if request.method=='POST':
        form_obj=CustomerForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse_url(request,'customer_list'))
    return render(request, 'consultant/add_customer.html', {'form_obj':form_obj})

def edit_customer(request,edit_id):
    obj=models.Customer.objects.filter(pk=edit_id).first()
    form_obj=CustomerForm(instance=obj)
    if request.method=='POST':
        form_obj = CustomerForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
        return redirect(reverse_url(request,'customer_list'))
    return render(request, 'consultant/edit_customer.html', {'form_obj': form_obj})

def customer_change(request,edit_id=None):
    obj=models.Customer.objects.filter(pk=edit_id).first()
    title='编辑客户' if edit_id else '新增客户'
    form_obj=CustomerForm(instance=obj)
    if request.method=='POST':
        form_obj = CustomerForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
        return redirect(reverse('customer_list'))
    return render(request, 'consultant/customer_change.html', {'form_obj': form_obj, 'title':title})

