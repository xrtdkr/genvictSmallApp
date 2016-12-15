# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from genvicSmallApp.settings import WECHAT_APPID, WECHAT_SECRET
from old_driver.models import WxUser, Group
from tools import *
import urllib2
import json
from urllib import urlencode

SUCCESS = 'success'


# Create your views here.

def wechat_login(request):
    '''
    流程是这样的，前端请求到了session_key和open_id，所以它把code给我们，我们也请求到了openid和session_key，所以我们就可以用
    微信所持有的session_key作为用户的session状态使用。即：登录中，未登录。
    '''
    try:

        f = open("wechat_log.txt", "a+")
        f.write("============wechat start===========\n")

        # 请求session_key_user
        code = request.POST.get('code', '')
        f.write('code: ' + code + '\n')

        # 请求session_key_wxserver
        access_token_req_dict = {
            'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        session_key_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' + urlencode(access_token_req_dict)
        f.write('session_key_url: ' + session_key_url + '\n')
        session_key_ret = urllib2.urlopen(session_key_url).read()
        f.write('session_key_ret: ' + session_key_ret + '\n')
        session_key_dict = json.loads(session_key_ret)
        openid = session_key_dict['openid']
        session_key_wxserver = session_key_dict['session_key']
        try:
            # ''' 数据库里面已经有现成的用户 '''
            user = WxUser.objects.get(wx_openid=openid)
            user.session = session_key_wxserver
            f.close()
            return JsonResponse({'status': 'login success,找到了已经有的用户', 'sessionKey': session_key_wxserver})
        except:

            # ''' 数据库中没有现成的用户 '''
            user = WxUser.objects.create(wx_openid=openid, session=session_key_wxserver)
            f.close()
            return JsonResponse({'status': 'login success,创建了一个新的用户', 'sessionKey': session_key_wxserver})
    except:
        f = open("wechat_test.txt", "a+")
        f.write('login failure')
        f.close()
        return HttpResponse("login failure, denglujiushishibaile")


def upload_init(request):
    try:
        session_key = request.POST.get('sessionKey', '')

        user = WxUser.objects.get(session_key=session_key)
        user_info = request.POST.get('userInfo')
        openid = user_info['openId']
        nick_name = user_info['nickName']
        gender = user_info['gender']
        province = user_info['province']
        icon = user_info['avatarUrl']

        user.wx_nickname = nick_name
        user.gender = gender
        user.province = province
        user.icon_url = icon
        user.save()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'fail'})


@require_POST
def new_group(request):
    try:
        session_upload = request.POST.get('session', '')
        try:
            user = WxUser.objects.get(session=session_upload)
            group_id = random_num_string()

            while not (Group.objects.filter(group_id=group_id)):
                group_id = random_num_string()

            group = WxUser.objects.create(group_id=random_num_string())
            longitude = request.POST.get('longitude', '')
            latitude = request.POST.GET('latitude', '')
            # group 创建成功

            user.longitude = longitude
            user.latitude = latitude
            user.group = group
            user.isLeader = True
            user.order_in_group = 0
            user.save()
            # user 更新成功
            return JsonResponse({'status': 'success', 'groupID': group_id})
        except:
            return JsonResponse({'status': 'fail'})
    except:
        return JsonResponse({'status': 'fail'})


@require_POST
def join_group(request):
    session_upload = request.POST.get('session', '')

    try:
        ''' 处理没有带session的错误 '''
        session_upload = request.POST.get('session', '')

        try:
            ''' 处理没有对应的session的错误 '''
            user = WxUser.objects.get(session=session_upload)
            longitude = request.POST.get('longitude', '')
            latitude = request.POST.GET('latitude', '')
            group_id = request.POST.get('groupID', '')

            group = Group.objects.get(group_id=group_id)
            user.longitude = longitude
            user.latitude = latitude
            user.isLeader = False
            user.group = group
            user.order_in_group = len(group.objects.all()) - 1
            user.save()

            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'fail'})
    except:
        return JsonResponse({'status': 'fail'})
