from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


# 验证访客是否登录
class VerifyMiddleware:

    def process_request(self, request):
        if 'user' not in request.session or not request.session['user']:
            path = request.path_info.lstrip('/')
        return