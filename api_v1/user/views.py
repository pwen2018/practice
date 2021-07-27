import json
from django.http import JsonResponse
from django.views import View
from user.models import UserProfile
from utils.encryption_MD5 import encryptionMD5
from utils.jwt_utils import create_token, get_user


# Create your views here.
class UserView(View):
    # 查询用户信息
    def get(self, request):
        username = get_user(request)
        user = UserProfile.objects.get(username=username)
        result = {'code': 200, "result": {"username": user.username, "nickname": user.nickname,
                                          "phone": user.phone}}
        return JsonResponse(result)

    # 注册用户
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10010, 'error': '用户名已存在'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 10011, 'error': '两次密码不一致'}
            return JsonResponse(result)
        password_h = encryptionMD5(password_1)
        token = create_token(username)
        try:
            UserProfile.objects.create(username=username, password=password_h,
                                       phone=phone, nickname=username)
        except Exception as e:
            print("create user error %s" % e)
            result = {'code': 10012, 'error': "用户已存在"}
            return JsonResponse(result)
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        return JsonResponse(result)

    # 更新用户信息
    def put(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = get_user(request)
        user = UserProfile.objects.get(username=username)
        user.nickname = json_obj['nickname']
        user.phone = json_obj['phone']
        # 判断用户是否传入密码参数
        if "old_password" in json_obj:
            # 修改密码前判断密码是否和数据库密码相同
            try:
                old_password = encryptionMD5(json_obj['old_password'])
                if old_password != user.password:
                    result = {'code': 10016, 'error': "密码错误"}
                    return JsonResponse(result)
                password = json_obj['new_password']
                user.password = encryptionMD5(password)
            except Exception as e:
                print('update password error %s' % e)
                result = {'code': 10017, 'error': "请输入密码"}
                return JsonResponse(result)
        user.save()
        token = create_token(username)
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        return JsonResponse(result)

    # 删除用户
    def delete(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = get_user(request)
        user = UserProfile.objects.get(username=username)
        if json_obj['cancellation'] == 0:
            # 注销前进行密码验证
            if user.password == encryptionMD5(json_obj['password']):
                user.cancellation = json_obj['cancellation']
                user.save()
                result = {'code': 200, 'data': '注销成功'}
                return JsonResponse(result)
        result = {'code': 10018, 'error': '注销失败'}
        return JsonResponse(result)


# 用户登录
def login(request):
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password = encryptionMD5(json_obj['password'])
        try:
            user = UserProfile.objects.get(username=username)
        except Exception as e:
            print('select error is %s' % e)
            result = {"code": 10016, 'error': '用户不存在'}
            return JsonResponse(result)
        if password != user.password:
            result = {'code': 10015, 'error': '用户名密码错误'}
            return JsonResponse(result)
        cancellation = user.cancellation
        if cancellation == 0:
            result = {'code': 10020, 'error': "用户已注销"}
            return JsonResponse(result)
        token = create_token(username)
        result = {"code": 200, "username": username, 'data': {"token": token}}
        return JsonResponse(result)

def get_test(request):
    return JsonResponse("测试拦截器")