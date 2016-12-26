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


class Album(models.Model):
    name = models.CharField(max_length=20, blank=True)
    album_id = models.CharField(max_length=50)
    user = models.ForeignKey(WxUser, null=True)  # 拥有这个相册的主人是谁

    def __unicode__(self):
        return self.name


class Image(models.Model):
    group = models.CharField(max_length=10, null=True)  # 这张image所处的组名。重复了就去死
    name = models.CharField(max_length=80, blank=True)  # name 是hash生成的一个名字
    url = models.CharField(max_length=100, blank=True)  # 在服务器里面的位置+上面的名字
    message = models.CharField(max_length=50, blank=True)  # 消息是消息
    user = models.ForeignKey(WxUser)  # 用户
    longitude = models.CharField(max_length=30, blank=True)
    latitude = models.CharField(max_length=30, blank=True)
    datetime = models.CharField(max_length=30, blank=True)  # 发送的时间
    album = models.ForeignKey(Album, null=True)

    def __unicode__(self):
        return self.name
