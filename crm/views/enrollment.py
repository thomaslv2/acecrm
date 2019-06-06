from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from django.views import View
from django.db.models import Q
from crm.utils.pagination import Pagination
from django.http.request import QueryDict
from crm.utils.urls import reverse_url
from crm.forms import EnrollmentForm


class EnrollmentList(View):
    def get(self, request):
        q = self.search([])
        all_enrollment = models.Enrollment.objects.filter(q, delete_status=False,
                                                          customer_id__in=[customer.pk for customer in
                                                                           request.user_obj.customers.all()])
        page = Pagination(request.GET.get('page'), all_enrollment.count(), request.GET.copy(), per_num=10)
        return render(request, 'consultant/enrollment_list.html',
                      {'all_enrollment': all_enrollment[page.start:page.end], 'page_html': page.page_html})

    def post(self, request):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        else:
            getattr(self, action)()
        return self.get(request)

    def search(self, fieldlist):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in fieldlist:
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


def enrollment_change(request, customer_id=None, enrollment_id=None):
    obj = models.Enrollment.objects.filter(pk=enrollment_id).first() if enrollment_id else models.Enrollment(
        customer_id=customer_id)
    form_obj = EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse_url(request, 'enrollment_list'))
    title = '编辑报名记录' if enrollment_id else '新增报名记录'
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})
