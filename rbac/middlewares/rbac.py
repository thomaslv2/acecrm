from django.utils.deprecation import MiddlewareMixin
from ace_crm.settings import PERMISSION_SESSION_KEY,WHITE_LIST,NO_PERMISSION_LIST
import re
from django.shortcuts import HttpResponse,redirect,reverse

class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):
        url=request.path_info
        for i in WHITE_LIST:
            if re.match(i,url):
                return
        request.current_menu_id=None
        request.breadcrumb_list=[{'title':'首页','url':reverse('index')}]
        #BC7737066F34

        for i in NO_PERMISSION_LIST:
            if re.match(i,url):
                return
        permission_dict=request.session.get(PERMISSION_SESSION_KEY)
        for item in permission_dict.values():
            #url pid id
            # print('^{}$'.format(i['permissions__url']))

            if re.match(r'^{}$'.format(item['url']),url):
                pid=item['pid']
                pname=item['pname']
                id=item['id']
                if pid:
                    request.current_menu_id=pid

                    request.breadcrumb_list.append({'title':permission_dict[pname]['title'],'url':permission_dict[pname]['url']})
                    request.breadcrumb_list.append({'title':item['title'],'url':item['url']})

                else:
                    request.current_menu_id=id
                    request.breadcrumb_list.append({'title':item['title'],'url':item['url']})
                return None
        return HttpResponse('没有访问权限！')
