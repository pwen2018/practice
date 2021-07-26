from django.http import JsonResponse
import json

from utils.jwt_utils import verify_bearer_token

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

write_list = [
    '/v1/user'
]


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in write_list:
            try:
                token = request.META.get('HTTP_AUTHORIZATION')
                token_list = token.replace('Bearer ', '')
            except:
                return JsonResponse({'tips': '您未登录', 'status': 402})
            try:
                if verify_bearer_token(token_list):
                    pass
                else:
                    return JsonResponse({'tips': '您未登录,登录信息过期', 'status': 401})
            except Exception as e:
                print(e)


