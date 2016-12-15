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
blank_group = Group.objects.get(group_id='')


# Create your views here.

def wechat_login(request):
    '''
    流程是这样的，前端请求到了session_key和open_id，所以它把code给我们，我们也请求到了openid和session_key，所以我们就可以用
    微信所持有的session_key作为用户的session状态使用。即：登录中，未登录。
    '''
    try:

        # f = open("wechat_log.txt", "a+")
        # f.write("============wechat start===========\n")

        # f.write('request-body: ' + request.body + '\n')
        data = json.loads(request.body)
        # 请求session_key_user
        code = data['code']
        # f.write('code: ' + code + '\n')
        # 请求session_key_wxserver
        access_token_req_dict = {
            'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        session_key_url = 'https://api.weixin.qq.com/sns/jscode2session?' + urlencode(access_token_req_dict)
        # f.write('session_key_url: ' + session_key_url + '\n')
        session_key_ret = urllib2.urlopen(session_key_url).read()
        # f.write('session_key_ret: ' + session_key_ret + '\n')

        session_key_dict = json.loads(session_key_ret)

        openid = session_key_dict['openid']
        session_key_wxserver = session_key_dict['session_key']

        # f.write('openid:' + openid + '\n')
        # f.write('session_key_wxserver:' + session_key_wxserver + '\n')
        try:
            ''' 数据库里面已经有现成的用户 '''
            # f.write('choice1'+'\n')
            user = WxUser.objects.get(wx_openid=openid)
            user.session = session_key_wxserver
            user.save()
            # f.close()
            return JsonResponse({'status': 'login success,找到了已经有的用户', 'sessionKey': session_key_wxserver})
        except:
            # f.write('choice2'+'\n')
            # ''' 数据库中没有现成的用户 '''
            user = WxUser.objects.create(wx_openid=openid, session=session_key_wxserver, group=blank_group)
            # f.close()
            user.save()
            return JsonResponse({'status': 'login success,创建了一个新的用户', 'sessionKey': session_key_wxserver})
    except:
        # f = open("wechat_test.txt", "a+")
        # f.write('login failure')
        # f.close()
        return HttpResponse("login failure, denglujiushishibaile")


def upload_init(request):
    try:
        f = open('upload_init.txt', 'a+')
        f.write('=====logging start=====\n')
        data = json.loads(request.body)
        f.write('data: ' + str(data) + '\n')
        session = data['session']
        # f.write('session1: ' + session + '\n')
        # f.write('session in database : ')
        for user in WxUser.objects.all():
            f.write(user.session)

        try:
            user = WxUser.objects.get(session=session)

            f.write('get user \n')

            user_info = data['userInfo']

            f.write('user_info: ' + str(user_info) + '\n')
            nick_name = user_info['nickName']
            gender = user_info['gender']
            province = user_info['province']
            icon = user_info['avatarUrl']

            user.wx_nickname = nick_name
            user.gender = gender
            user.province = province
            user.icon_url = icon
            user.save()
            f.write(' user init success' + '\n')
            f.close()
            return JsonResponse({'status': 'success'})
        except:
            f.write('choice1' + '\n')
            f.close()
            return JsonResponse({'status': 'fail'})
    except:
        f.write('choice2' + '\n')
        f.close()
        return JsonResponse({'status': 'fail'})


def new_group(request):
    f = open('new_group.txt', 'a+')
    f.write('========= log ==========')
    try:
        data = json.loads(request.body)
        f.write('data: ' + str(data) + '\n')
        session_upload = data['session']
        f.write('session: ' + session_upload + '\n')
        for user in WxUser.objects.all():
            f.write(user.session)

        try:
            user = WxUser.objects.get(session=session_upload)
            f.write('user get \n')

            if user.group.group_id:
                return JsonResponse({'status': 'fail, user has in a group'})
            else:
                group_id = random_num_string()

                f.write('group_id: ' + group_id + '\n')

                group = Group.objects.create(group_id=group_id)

                longitude = data['longitude']
                latitude = data['latitude']
                # group 创建成功

                user.longitude = longitude
                user.latitude = latitude
                user.group = group
                user.isLeader = True
                user.order_in_group = 0
                user.save()
                f.write('new group success')
                # user 更新成功
                return JsonResponse({'status': 'success', 'groupID': group_id})
        except:
            return JsonResponse({'status': 'fail'})
    except:
        return JsonResponse({'status': 'fail'})


def join_group(request):
    try:
        data = json.loads(request.body)
        ''' 处理没有带session的错误 '''
        session_upload = data['session']

        try:
            ''' 处理没有对应的session的错误 '''
            user = WxUser.objects.get(session=session_upload)

            if user.group.group_id:
                return JsonResponse({'status': 'fail', 'reason': '已经加入了其他小队'})

            longitude = data['longitude']
            latitude = data['latitude']
            group_id = data['groupID']

            group = Group.objects.get(group_id=group_id)
            user.longitude = longitude
            user.latitude = latitude
            user.isLeader = False
            user.group = group
            user.order_in_group = len(group.objects.all())
            user.save()

            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'fail', 'reason': 'session reveal no user'})
    except:
        return JsonResponse({'status': 'fail'})


def refresh(request):
    f = open('refresh.txt', 'a+')

    try:
        data = json.loads(request.body)
        session_upload = data['session']
        try:
            user = WxUser.objects.get(session=session_upload)

            # 已经查找到了已有用户

            longitude = data['longitude']
            latitude = data['latitude']
            state = data['state']

            # save the attr
            user.longitude = longitude
            user.latitude = latitude
            user.state = state

            group_id = user.group.group_id

            try:
                # 找到了用户ID
                f.write('找到了用户ID \n')
                group = Group.objects.get(group_id=group_id)

                ret_data = {}
                ret_data['isDismiss'] = False
                ret_data['user'] = []
                for user in group.wxuser_set:
                    user_dict = {}
                    user_dict['nickname'] = user.wx_nickname
                    user_dict['iconurl'] = user.icon_url
                    user_dict['state'] = user.state
                    user_dict['order'] = user.order_in_group
                    user_dict['isLeader'] = user.isLeader
                    user_dict['longitude'] = user.longitude
                    user_dict['latitude'] = user.latitude
                    ret_data['user'].append(user_dict)
                    f.write('user_dict: ' + str(user_dict) + '\n')

                f.write('ret_data: ' + str(ret_data) + '\n')
                return JsonResponse(ret_data)
            except:
                return JsonResponse({'isDismiss': True, 'user': []})

        except:
            return JsonResponse({'status': 'fail'})

    except:
        return JsonResponse({'status': 'fail'})


def dismiss(request):
    try:
        data = json.loads(request.body)
        session_upload = data['session']
        try:
            user = WxUser.objects.get(session=session_upload)
            group_id = user.group.group_id
            if user.isLeader == True:
                Group.objects.get(group_id=group_id).delete()
                return JsonResponse({'status': 'success, leader dismiss'})

            else:
                user.group = blank_group
                user.save()
                return JsonResponse({'status': 'success, member logout'})
        except:
            return JsonResponse({'status': 'fail'})
    except:
        return JsonResponse({'status': 'fail'})
