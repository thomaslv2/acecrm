from django import forms
from crm import models
from django.core.exceptions import ValidationError


class BSForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form_control'})


class RegForm(BSForm):
    # password=forms.CharField(widget=forms.PasswordInput,min_length=6)
    re_pwd = forms.CharField(widget=forms.PasswordInput(), min_length=6, label='确认密码')

    class Meta:
        model = models.UserProfile
        fields = '__all__'  # ['username','password']   #'__all__'
        exclude = ['memo', 'is_active']
        labels = {
            'username': '用户名'
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form_control'})
        }

    def clean(self):
        password = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')
        if password == re_pwd:
            return self.cleaned_data
        self.add_error('re_pwd', '两次密码不一致')
        raise ValidationError('两次密码不一致')


class CustomerForm(BSForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.pop('class')


class ConsultForm(BSForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_choices = [(customer.pk, str(customer)) for customer in self.instance.consultant.customers.all()]
        customer_choices.insert(0, ('', '---------'))
        self.fields['customer'].choices = customer_choices
        self.fields['consultant'].choices = [('', '---------'),
                                             (self.instance.consultant.pk, str(self.instance.consultant))]


class EnrollmentForm(BSForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'].choices = [(self.instance.customer.pk, str(self.instance.customer))]
        # self.fields['enrolment_class'].choices=[(i.pk,str(i)) for i in self.instance.customer.class_list.all()]


class ClassForm(BSForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'


class CourseRecordForm(BSForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['re_class'].choices = [(self.instance.re_class.pk, str(self.instance.re_class))]
        self.fields['teacher'].choices = [(self.instance.teacher.pk, str(self.instance.teacher))]


# class StudyRecordForm(BSForm):
#     class Meta:
#         model = models.StudyRecord
#         fields = '__all __'


class StudyRecordForm(BSForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'
