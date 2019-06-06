from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.forms import RegForm
from rbac.service.permission import init_permission


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj=models.UserProfile.objects.filter(username=username, password=password, is_active=True).first()
        if obj:
            request.session['pk']=obj.pk
            init_permission(obj,request)
            return redirect(reverse('customer_list'))

    return render(request, 'login.html')


def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        print('zouzhele')
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
        return redirect(reverse('login'))
    return render(request, 'reg.html', {'form_obj': form_obj})