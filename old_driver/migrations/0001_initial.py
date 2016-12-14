# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WxUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wx_openid', models.CharField(max_length=100)),
                ('session', models.CharField(max_length=100)),
                ('login_flag', models.BooleanField(default=False)),
                ('wx_icon', models.CharField(max_length=100)),
                ('wx_nickname', models.CharField(max_length=20)),
                ('gender', models.IntegerField(default=1, blank=True)),
                ('province', models.CharField(max_length=10)),
                ('icon_url', models.CharField(max_length=200)),
                ('longitude', models.CharField(default=b'103.930662', max_length=20)),
                ('latitude', models.CharField(default=b'30.748775', max_length=20)),
                ('state', models.CharField(default=b'\xe5\xbe\x88\xe9\xab\x98\xe5\x85\xb4\xe8\xa7\x81\xe5\x88\xb0\xe5\xa4\xa7\xe5\xae\xb6', max_length=100)),
                ('isLeader', models.BooleanField(default=False)),
                ('order_in_group', models.IntegerField(default=0)),
                ('group', models.ForeignKey(related_name='group', blank=True, to='old_driver.Group')),
            ],
        ),
    ]
