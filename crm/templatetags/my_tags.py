from django.template import Library
register=Library()

from django.urls import reverse
from django.http.request import QueryDict
@register.simple_tag
def reverse_url(request,name,*args,**kwargs):
    base_path=reverse(name,args=args,kwargs=kwargs)
    next=request.get_full_path()
    dict=QueryDict(mutable=True)
    dict['next']=next
    return '{}?{}'.format(base_path,dict.urlencode())
    