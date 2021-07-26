from django.db import models


# Create your models here.
class UserProfile(models.Model):
    """
    auto_now_add: 字段在实例第一次保存的时候会保存当前时间,不管你在这里是否对其赋值。
    但是之后的save()是可以手动赋值的。也就是新实例化一个model,想手动存其他时间,
    就需要对该实例save()之后赋值然后再save()。
    auto_now: 字段保存时会自动保存当前时间，但要注意每次对其实例执行save()的时候都会将当前时间保存，
    也就是不能再手动给它存非当前时间的值。
    """
    id = models.BigAutoField(verbose_name="自增ID", primary_key=True, db_column='id')
    username = models.CharField(verbose_name="用户名", max_length=20, db_column='username')
    password = models.CharField(verbose_name="密码", max_length=50, db_column='passwrod')
    nickname = models.CharField(verbose_name="昵称", max_length=20, null=True, db_column='nickname')
    phone = models.CharField(verbose_name="手机号", max_length=11, db_column='phone')
    # 0代表用户注销账户 1代表用户正常使用
    cancellation = models.IntegerField(verbose_name="用户逻辑删除", default=1, db_column='cancellation')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, db_column='create_time')
    update_time = models.DateTimeField(verbose_name="创建时间", auto_now=True, db_column='update_time')
