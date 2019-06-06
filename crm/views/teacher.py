from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.forms import ClassForm,CourseRecordForm,StudyRecordForm
from django.views import View
from django.db.models import Q
from crm.utils.pagination import Pagination
from django.http.request import QueryDict
from crm.utils.urls import reverse_url
from django.db import transaction
from ace_crm.settings import MAX_CUSTOMER_NUM


class ClassList(View):

    def get(self, request):

        q = self.search([])
        # 班级展示
        all_class = models.ClassList.objects.filter(q)
        page = Pagination(request.GET.get('page'), all_class.count(), request.GET.copy(), per_num=10)
        return render(request, 'teacher/class_list.html',
                      {'all_class': all_class[page.start:page.end], 'page_html': page.page_html})

    def post(self, request):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        else:
            ret = getattr(self, action)()
            if ret:
                return ret
        return self.get(request)

    def search(self, fieldlist):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in fieldlist:
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q


def class_change(request, edit_id=None):
    obj = models.ClassList.objects.filter(pk=edit_id).first()
    title = '编辑班级' if edit_id else '新增班级'
    form_obj = ClassForm(instance=obj)
    if request.method == 'POST':
        form_obj = ClassForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
        return redirect(reverse('class_list'))
    return render(request, 'teacher/class_change.html', {'form_obj': form_obj, 'title': title})


class CourseRecordList(View):
    def get(self, request, class_id):
        q = self.search([])
        # 班级展示
        all_class_record = models.CourseRecord.objects.filter(q, re_class=class_id)
        page = Pagination(request.GET.get('page'), all_class_record.count(), request.GET.copy(), per_num=10)
        return render(request, 'teacher/course_record_list.html',
                      {'class_id':class_id,'all_class_record': all_class_record[page.start:page.end], 'page_html': page.page_html})

    def post(self, request, class_id):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        else:
            ret = getattr(self, action)()
            if ret:
                return ret
        return self.get(request, class_id)

    def search(self, fieldlist):
        query = self.request.GET.get('query', '')
        # q = Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'
        for field in fieldlist:
            q.children.append(Q(('{}__contains'.format(field), query)))
        return q
    
    def multi_init(self):
        #先拿课程记录id
        course_record_ids=self.request.POST.getlist('ids')
        for course_record_id in course_record_ids:
            course_record=models.CourseRecord.objects.filter(pk=course_record_id).first()
            all_student=course_record.re_class.customer_set.filter(status='studying')
            for student in all_student:
                models.StudyRecord.objects.get_or_create(course_record=course_record,student=student)



def courserecord_change(request, class_id=None, courserecord_id=None):
    obj = models.CourseRecord.objects.filter(pk=courserecord_id).first() if courserecord_id else models.CourseRecord(
        re_class_id=class_id, teacher=request.user_obj)
    title = '编辑课程记录' if courserecord_id else '新增课程记录'
    form_obj = CourseRecordForm(instance=obj)
    if request.method == 'POST':
        form_obj = CourseRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
        return redirect(reverse_url(request,'courserecord_list',class_id))
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

from django.forms import modelformset_factory

def studyrecordlist(request,courserecord_id):
    FormSet=modelformset_factory(models.StudyRecord,StudyRecordForm,extra=0)
    all_studyrecord=models.StudyRecord.objects.filter(course_record_id=courserecord_id)
    form_obj=FormSet(queryset=all_studyrecord)
    if request.method=='POST':
        form_obj=FormSet(request.POST)
        if form_obj.is_valid():
            form_obj.save()
    return render(request,'teacher/study_record_list.html',{'form_obj':form_obj})