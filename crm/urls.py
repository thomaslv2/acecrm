from django.conf.urls import url
from crm import views
from crm.views import customer,auth,consult,enrollment,teacher

urlpatterns = [
    url(r'^customer_list/', customer.CustomerList.as_view(),name='customer_list'),
    
    url(r'^mycustomer/', customer.CustomerList.as_view(),name='mycustomer'),
    # url(r'^user_list/', views.user_list),
    url(r'^add_customer/', customer.add_customer,name='add_customer'),
    # url(r'^add_customer/', customer.customer_change,name='add_customer'),
    # 编辑客户
    url(r'^edit_customer/(\d+)', customer.edit_customer,name='edit_customer'),
    # url(r'^edit_customer/(\d+)', customer.customer_change,name='edit_customer'),
    url(r'^consult_list/(0)', consult.ConsultList.as_view(), name='all_consult_list'),
    url(r'^consult_list/(?P<customer_id>\d+)', consult.ConsultList.as_view(), name='consult_list'),

    url(r'^add_consult/', consult.add_consult, name='add_consult'),
    url(r'^edit_consult/(\d+)', consult.edit_consult, name='edit_consult'),

    url(r'^enrollment_list/', enrollment.EnrollmentList.as_view(), name='enrollment_list'),

    url(r'^add_enrollment/(?P<customer_id>\d+)', enrollment.enrollment_change, name='add_enrollment'),
    url(r'^edit_enrollment/(?P<enrollment_id>\d+)', enrollment.enrollment_change, name='edit_enrollment'),
    #班级展示
    url(r'^class_list/', teacher.ClassList.as_view(), name='class_list'),
    #班级添加与修改
    url(r'^add_class/', teacher.class_change, name='add_class'),
    url(r'^edit_class/(\d+)', teacher.class_change, name='edit_class'),
    #展示上课记录
    url(r'^courserecord_list/(?P<class_id>\d+)', teacher.CourseRecordList.as_view(), name='courserecord_list'),
    #上课记录添加与修改
    url(r'^add_courserecord/(?P<class_id>\d+)', teacher.courserecord_change, name='add_courserecord'),
    url(r'^edit_courserecord/(?P<courserecord_id>\d+)', teacher.courserecord_change, name='edit_courserecord'),
    #展示学习记录
    url(r'^studyrecord_list/(?P<courserecord_id>\d+)', teacher.studyrecordlist, name='studyrecord_list'),

]