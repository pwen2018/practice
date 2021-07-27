import logging
from django.http import JsonResponse
from utils.jwt_utils import verify_bearer_token

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

write_list = [
    '/v1/user/', '/v1/user/login/'
]
logger = logging.getLogger(__name__)

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in write_list:
            try:
                token = request.META.get('HTTP_AUTHORIZATION')
                token_list = token.replace('Bearer ', '')
            except:
                return JsonResponse({'code': 402, 'data': '您未登录', })
            try:
                if verify_bearer_token(token_list):
                    pass
                else:
                    return JsonResponse({'code': 401, 'data': '您未登录,登录信息过期'})
            except Exception as e:
                result = {'code': 401, 'data': '无效token'}
                return JsonResponse(result)
