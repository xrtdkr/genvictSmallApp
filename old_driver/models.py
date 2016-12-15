# coding=utf-8
from django.db import models


# Create your models here.

class Group(models.Model):
    ''' 组 '''

    group_id = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.group_id


class WxUser(models.Model):
    ''' 微信的用户模块 '''

    ''' 唯一验证信息 '''
    wx_openid = models.CharField(max_length=100)
    session = models.CharField(max_length=100)

    ''' 基本信息 '''
    # wx_icon = models.CharField(max_length=100, blank=True)  # 用来存储用户的头像
    wx_nickname = models.CharField(max_length=20, blank=True)  # 用来存储用户的昵称
    gender = models.IntegerField(default=1, blank=True)  # 用户的性别，留作接口，1是男生，0是女生
    province = models.CharField(max_length=10, blank=True)
    icon_url = models.CharField(max_length=200, blank=True)  # 对应的是微信里面的AVATARURL

    ''' 应用信息 '''
    longitude = models.CharField(max_length=20, default='103.930662')
    latitude = models.CharField(max_length=20, default='30.748775')
    state = models.CharField(max_length=100, default='很高兴见到大家')
    isLeader = models.BooleanField(default=False)
    group = models.ForeignKey(Group)
    order_in_group = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.wx_openid
