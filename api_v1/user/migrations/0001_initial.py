# Generated by Django 2.2.16 on 2021-07-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='自增ID')),
                ('username', models.CharField(db_column='username', max_length=20, verbose_name='用户名')),
                ('password', models.CharField(db_column='passwrod', max_length=50, verbose_name='密码')),
                ('nickname', models.CharField(db_column='nickname', max_length=20, null=True, verbose_name='昵称')),
                ('phone', models.CharField(db_column='phone', max_length=11, verbose_name='手机号')),
                ('cancellation', models.IntegerField(db_column='cancellation', default=1, verbose_name='用户逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='create_time', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, db_column='update_time', verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user',
            },
        ),
    ]
