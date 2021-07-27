import jwt
import time
from django.conf import settings

# 使用 sanic 作为restful api 框架
from django.http import JsonResponse


def create_token(username):
    payload = {
        "iss": "com.sven",
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,
        "username": username,
    }
    token = jwt.encode(payload, settings.JWT_TOKEN_KEY, algorithm='HS256')
    return token


def verify_bearer_token(token):
    #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
    payload = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms=['HS256'])
    if payload:
        return payload
    result = {'code': 10014, 'error': "token失效"}
    return JsonResponse(result)


def get_user(request):
    token = request.META.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
    user = verify_bearer_token(token)
    username = user["username"]
    return username

