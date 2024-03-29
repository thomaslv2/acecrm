from django.contrib.auth.middleware import AuthenticationMiddleware
from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin
from crm import models


class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info in [reverse('login'), reverse('reg')] or request.path_info.startswith('/admin/'):
            return

        pk = request.session.get('pk')
        # print(pk)
        obj = models.UserProfile.objects.filter(pk=pk).first()
        if obj:
            request.user_obj = obj
            return
        return redirect(reverse('login'))


