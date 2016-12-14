# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from genvicSmallApp.settings import WECHAT_APPID, WECHAT_SECRET
from old_driver.models import WxUser, Group
from tools import *


# Create your views here.

def wechat_login(request):
    try:
        f = open("wechat_test.txt", "a+")
        f.write("============wechat start===========\n")
        code = request.GET['code']
        f.write('code: ' + code + '\n')

        access_token_req_dict = {
            'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
        }

        address_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' + urlencode(access_token_req_dict)
        f.write('address_token_url: ' + address_token_url + '\n')

        access_token_ret = urllib2.urlopen(address_token_url).read()
        f.write('access_token_url: ' + access_token_ret + '\n')

        access_token_dict = json.loads(access_token_ret)
        access_token = access_token_dict['access_token']
        expires_in = access_token_dict['expires_in']
        openid = access_token_dict['openid']
        scope = access_token_dict['scope']

        tmp_dict = {
            'access_token': access_token,
            'openid': openid,
        }
        address3 = 'https://api.weixin.qq.com/sns/userinfo?' + urlencode(tmp_dict)

        wx_user_info = urllib2.urlopen(address3).read()

        wx_user = json.loads(wx_user_info)
        nickname = wx_user['nickname']
        openid = wx_user['openid']
        headimgurl = wx_user['headimgurl']

        f.write('wx_user_info: ' + wx_user_info + '\n')
        f.close()

        current_user = TmpUser(username=nickname, icon=headimgurl)
        return render_to_response('frontEnd/account.html', {'login_flag': True, 'current_user': current_user},
                                  context_instance=RequestContext(request))
    except:
        f = open("wechat_test.txt", "a+")
        f.write('login failure')
        f.close()
        return HttpResponse("login failure")


@require_POST
def new_group(request):
    try:
        session_upload = request.POST.get('session', '')
        try:
            user = WxUser.objects.get(session=session_upload)
            group_id=random_num_string()

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
            user.order_in_group = len(group.objects.all())-1
            user.save()

            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'fail'})
    except:
        return JsonResponse({'status': 'fail'})




