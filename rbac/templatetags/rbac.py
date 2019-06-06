from django import template
register=template.Library()
from django.conf import settings
import re
from collections import OrderedDict

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_dict=request.session.get(settings.MENU_SESSION_KEY)
    # print(menu_dict,type(menu_dict))
    order_dict=OrderedDict()
    # for item in menu_dict.values():
    for key in sorted(menu_dict,key=lambda i:menu_dict[i]['weight'],reverse=True):
        order_dict[key]=item=menu_dict[key]
        item['class']='hide'
        for i in item['children']:
            # if re.match('^{}$'.format(i['url']),request.path_info):
            if i['id']==request.current_menu_id:
                i['class']='active'
                item['class'] = ''
                break

    return {'menu_dict':order_dict.values()}

@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'breadcrumb_list':request.breadcrumb_list}

@register.filter
def has_permission(request,name):
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params['rid'] = rid
    return params.urlencode()
