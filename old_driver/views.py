# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from genvicSmallApp.settings import WECHAT_APPID, WECHAT_SECRET
from old_driver.models import WxUser, Group, Image, Album
from tools import *
import urllib2
import json
from urllib import urlencode, unquote
from django.db.models import Q
from itertools import chain
from django.db.models.query import QuerySet
from django.utils import datetime_safe
import datetime


SUCCESS = 'success'
blank_group = Group.objects.get(group_id='')


# Create your views here.

def wechat_login(request):
    '''
    流程是这样的，前端请求到了session_key和open_id，所以它把code给我们，我们也请求到了openid和session_key，所以我们就可以用
    微信所持有的session_key作为用户的session状态使用。即：登录中，未登录。
    '''
    print '=================wechat_login==============='
    try:

        # f = open("wechat_log.txt", "a+")
        # f.write("============wechat start===========\n")
        # f.write('request-body: ' + request.body + '\n')
        data = json.loads(request.body)
        # 请求session_key_user
        code = data['code']
        # code = request.POST.get('code', '')
        print '=====code==='
        print code
        # f.write('code: ' + code + '\n')
        # 请求session_key_wxserver
        access_token_req_dict = {
            'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code',
        }

        print 'access_token_req_dict:' + str(access_token_req_dict) + '\n'
        session_key_url = 'https://api.weixin.qq.com/sns/jscode2session?' + urlencode(access_token_req_dict)
        # f.write('session_key_url: ' + session_key_url + '\n')
        session_key_ret = urllib2.urlopen(session_key_url).read()
        # f.write('session_key_ret: ' + session_key_ret + '\n')

        session_key_dict = json.loads(session_key_ret)

        openid = session_key_dict['openid']
        session_key_wxserver = session_key_dict['session_key']

        print 'session: ' + session_key_wxserver
        # f.write('openid:' + openid + '\n')
        # f.write('session_key_wxserver:' + session_key_wxserver + '\n')
        try:
            ''' 数据库里面已经有现成的用户 '''
            # f.write('choice1'+'\n')
            user = WxUser.objects.get(wx_openid=openid)
            group_id = user.group.group_id
            user.session = session_key_wxserver
            user.save()
            # f.close()
            return JsonResponse(
                {'status': 'login success,找到了已经有的用户', 'sessionKey': session_key_wxserver, 'groupID': group_id})
        except:
            # f.write('choice2'+'\n')
            # ''' 数据库中没有现成的用户 '''
            user = WxUser.objects.create(wx_openid=openid, session=session_key_wxserver, group=blank_group)
            group_id = user.group.group_id
            return JsonResponse(
                {'status': 'login success,创建了一个新的用户', 'sessionKey': session_key_wxserver, 'groupID': group_id})
    except:
        # f = open("wechat_test.txt", "a+")
        # f.write('login failure')
        # f.close()
        return JsonResponse({'status': 'login fail, login fail'})


def upload_init(request):
    try:
        print '==========upload_init==============='

        data = json.loads(request.body)
        session = data['session']
        print 'session: '
        print session
        # session = request.POST.get('session', '')

        for user in WxUser.objects.all():
            print 'user.session: ' + user.session
            print 'session up is same'

        try:
            user = WxUser.objects.get(session=session)

            # f.write('get user \n')

            user_info = data['userInfo']
            # user_info = request.POST.get('userInfo', '')
            print 'user_info: '
            print user_info
            nick_name = user_info['nickName']
            gender = user_info['gender']
            province = user_info['province']
            icon = user_info['avatarUrl']

            user.wx_nickname = nick_name
            user.gender = gender
            user.province = province
            user.icon_url = icon
            user.save()
            print 'user init success'
            # f.close()
            return JsonResponse({'status': 'success'})
        except:
            # f.write('choice1' + '\n')
            # f.close()
            return JsonResponse({'status': 'fail'})
    except:
        # f.write('choice2' + '\n')
        # f.close()
        return JsonResponse({'status': 'fail'})


def change_state(request):
    try:
        data = json.loads(request.body)

        print 'data: '
        print data

        session_upload = data['session']

        try:
            user = WxUser.objects.get(session=session_upload)
            print user.wx_nickname

            state = data['state']
            user.state = state
            user.save()
            print 'save success...'

            return JsonResponse({'status': 'success'})

        except:
            return JsonResponse({'status': 'fail, aaaaa'})

    except:
        return JsonResponse({'status': 'fail,bbbbbb'})


def new_group(request):
    print '======new_group======'
    try:
        data = json.loads(request.body)
        session_upload = data['session']
        print 'session: '
        print session_upload
        # session_upload = request.POST.get('session', '')
        # for user in WxUser.objects.all():
        #     f.write(user.session)
        try:
            user = WxUser.objects.get(session=session_upload)
            print 'user: '
            print user

            group_id = user.group.group_id
            print 'group_id: '
            print group_id

            if group_id:
                print 'group id is '
                return JsonResponse({'status': 'fail, user has in a group', 'groupID': group_id})
            else:
                group_id = random_num_string()
                group = Group.objects.create(group_id=group_id)

                longitude = data['longitude']
                # longitude = request.POST.get('longitude', '')
                latitude = data['latitude']
                # latitude = request.POST.get('latitude', '')
                print 'group init success'

                user.longitude = longitude
                user.latitude = latitude
                user.group = group
                user.isLeader = True
                user.order_in_group = 0
                user.save()

                print 'user chuang jian cheng gong'
                return JsonResponse({'status': 'success', 'groupID': group_id})
        except:
            return JsonResponse({'status': 'fail'})
    except:
        return JsonResponse({'status': 'fail'})


def join_group(request):
    print '=======join group start======='
    try:
        data = json.loads(request.body)
        ''' 处理没有带session的错误 '''
        session_upload = data['session']
        # session_upload = request.POST.get('session', '')

        try:
            ''' 处理没有对应的session的错误 '''
            user = WxUser.objects.get(session=session_upload)
            print user
            if user.group.group_id:
                print '已经加入了其他小队'
                return JsonResponse({'status': 'fail', 'reason': '已经加入了其他小队'})
            else:
                longitude = data['longitude']
                latitude = data['latitude']
                group_id = data['groupID']

                # longitude = request.POST.get('longitude', '')
                # latitude = request.POST.get('latitude', '')
                # group_id = request.POST.get('groupID', '')
                print group_id
                try:
                    print 'after try'

                    group = Group.objects.get(group_id=str(group_id))

                    # print group:
                    user.longitude = longitude
                    user.latitude = latitude
                    user.isLeader = False
                    user.group = group
                    user.order_in_group = len(group.wxuser_set.all())
                    user.save()
                    print 'join success'
                    return JsonResponse({'status': 'success'})
                except:
                    print 'no group exist'
                    return JsonResponse({'status': 'fail', 'reason': 'no group exist'})

        except:
            return JsonResponse({'status': 'fail', 'reason': 'session reveal no user'})
    except:
        return JsonResponse({'status': 'fail'})


def refresh(request):
    print '=======refresh========='
    try:
        data = json.loads(request.body)
        print data
        session_upload = data['session']
        print session_upload

        # session_upload = request.POST.get('session', '')
        try:
            user = WxUser.objects.get(session=session_upload)
            print user
            # 已经查找到了已有用户

            longitude = data['longitude']
            latitude = data['latitude']
            # state = data['state']
            group_id = data['groupID']
            # longitude = request.POST.get('longitude', '')
            # latitude = request.POST.get('latitude', '')
            # state = request.POST.get('state', '')
            # save the attr
            user.longitude = longitude
            user.latitude = latitude
            # user.state = state
            user.save()
            print group_id
            print 'user information update complete'
            try:
                # 找到了用户ID
                group = Group.objects.get(group_id=group_id)

                ret_data = {}
                ret_data['isDismiss'] = False
                ret_data['user'] = []
                print 'in loop'
                for user in group.wxuser_set.all():
                    user_dict = {}
                    user_dict['nickname'] = user.wx_nickname
                    user_dict['iconurl'] = user.icon_url
                    user_dict['state'] = user.state
                    user_dict['order'] = user.order_in_group
                    user_dict['isLeader'] = user.isLeader
                    user_dict['longitude'] = user.longitude
                    user_dict['latitude'] = user.latitude
                    ret_data['user'].append(user_dict)
                    print '======ret_data====='
                    print user_dict

                print '====ret_data===='
                print ret_data
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
        # session_upload = request.POST.get('session', '')
        try:
            user = WxUser.objects.get(session=session_upload)

            if user.isLeader == True:
                group_id = user.group.group_id
                user.group = blank_group
                user.save()
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


''' post 请求 '''


def refresh_pic(request):
    try:
        data = json.loads(request.body)
        session_upload = data['session']

        try:
            user = WxUser.objects.get(session=session_upload)
            print 'user'
            print user
            group_id = user.group.group_id
            print group_id
            group = Group.objects.get(group_id=group_id)
            print group
            user_set = group.wxuser_set.all()
            print user_set

            tmp_list = user.image_set.filter(group='888888')
            print 'yi ge kong de dong xi'
            print tmp_list

            print ' ji jiang jin ru xun huan'
            for user in user_set.all():
                set_image = user.image_set.filter(group=group_id)
                tmp_list = tmp_list | set_image
            tmp_list.all().order_by("datetime")
            print user_set.all()

            print 'print tmp_list, yong datetime lai zuo dong xi'
            ret_list = []
            for image in tmp_list.all():
                ret_dict = {}

                ret_dict['nickname'] = image.user.wx_nickname
                ret_dict['avator'] = image.user.icon_url
                ret_dict['content'] = image.message
                ret_dict['image'] = image.url
                ret_dict['publishTime'] = image.datetime
                ret_dict['latitude'] = image.latitude
                ret_dict['longitude'] = image.longitude

                ret_list.append(ret_dict)
            print 'ret_list: de yangshi yinggai yaohe jiekou wendang xiangtong:'
            print ret_list
            return JsonResponse({'image': ret_list})

        except:
            print 'beng2'
            return JsonResponse({'status': 'fail,but session got'})
    except:
        print 'beng1'
        return JsonResponse({'status': 'fail, session did not get'})


# 这边的请求头的content-type是multi

def new_pic(request):
    try:
        print '==========new_pic==========='
        session_upload = request.POST['session']
        print session_upload
        try:
            user = WxUser.objects.get(session=session_upload)
            print "session: " + user.session
            print " request.POST:  "
            print request.POST
            print "direct  "
            content = request.POST.get('content', '')
            print 'content: '
            print content
            # ==== = == = = == = beng = = ==
            latitude = request.POST['latitude']
            print "latitude: "
            print latitude
            longitude = request.POST['longitude']
            print 'longitude: '
            print longitude
            file_path = request.POST['filePath']

            print 'file_path: '
            print file_path
            image = request.FILES['file']
            print 'image: '
            print image
            print 'image get'
            group_id = user.group.group_id

            print 'group_id: '
            print group_id
            print '====log==='
            print content
            print latitude
            print longitude
            print type(image)
            print 'image receive is not down wow!'

            name = file_path.split("://")[1]
            print name
            file_url = 'picture/' + name
            url = 'https://ebichu.cn/picture/' + name
            print url

            print '=============='
            Image.objects.create(group=group_id, name=name, url=url, message=content, user=user, longitude=longitude,
                                 latitude=latitude, datetime=datetime_safe.datetime.now().strftime(("%Y-%m-%d %H:%M")))
            print '=============='

            print 'the picture ready to write: '
            f = open(file_url, 'wb')
            for chunk in image.chunks():
                f.write(chunk)
            f.close()
            print 'the image has been writen'

            print 'success'
            return JsonResponse({'status': 'success'})
        except:
            print 'session got but fail'
            return JsonResponse({'status': 'fail,but session got'})
    except:
        print "receive upload session fail"
        return JsonResponse({'status': 'fail,but did not session got'})


def create_album(request):
    '''
    request:
        session, albumName
    return:
        status
    '''
    print '======create_album======='
    try:
        data = json.loads(request.body)
        session_upload = data['session']
        try:
            user = WxUser.objects.get(session=session_upload)
            group_id = user.group.group_id
            if not group_id:
                print 'group id is blank'
                return JsonResponse({'status': 'fail, group id is blank'})
            else:
                print 'start to build album'

                album_name = data['albumName']
                print album_name
                album_id = hashlib.sha1(str(datetime.datetime.now())).hexdigest()
                print album_id
                album = Album.objects.create(name=album_name, album_id=album_id, user=user)
                print album
                images = Image.objects.filter(group=group_id)
                for image in images:
                    image.album = album
                    image.save()
                return JsonResponse({'status': 'success'})
        except:
            print 'no user get'
            return JsonResponse({'status': 'fail, no user get'})
    except:
        print 'no session get'
        return JsonResponse({'status': 'fail, no session get'})


def album_set(request):
    '''
    这个函数是用来查看相册集合的，一个单独的页面去显示相册的页面
    :param request: session
    :return: {
                "status":"success",
                "album":[
                    {
                        name: xxx,
                        id:   xxx,
                        image: xxx,
                        time: xxx,
                     }
                     ...
                     {
                        name: xxx,
                        id:   xxx,
                        image: xxx,
                        time: xxx,
                     }
            }
    '''

    try:
        data = json.loads(request.body)
        try:
            session_upload = data['session']

            user = WxUser.objects.get(session=session_upload)
            album_list = []
            for album in user.album_set.all():
                try:
                    image = album.image_set.all()[0]
                    ele = {}
                    ele['name'] = album.name
                    ele['id'] = album.album_id
                    ele['image'] = image.url
                    ele['time'] = image.datetime
                    album_list.append(ele)
                except:
                    pass
            if not album_list:
                return JsonResponse({'status': 'fail'})
            else:
                return JsonResponse({'status': 'success', 'album': album_list})
        except:
            print 'session got no user'
            return JsonResponse({'status': 'session got, with no user'})
    except:
        print 'no session got'
        return JsonResponse({'status': 'fail,but did not session got'})


def album_view(request):
    '''
    request: {session: xxx, albumID: xxx}
    return:{
            status:success
            image:[{
                    content: xxx,(mess)
                    image : xxx,(url)
                    longitude: xxx,
                    latitude: xxx,
                    time: xxx,
                }
                ...
                {
                    content: xxx,(mess)
                    image : xxx,(url)
                    longitude: xxx,
                    latitude: xxx,
                    time: xxx,
                }]
            }

    '''
    try:
        print '========album_view======='
        data = json.loads(request.body)
        print data

        try:
            session_upload = data['session']
            print session_upload
            user = WxUser.objects.get(session=session_upload)
            print user
            album_id = data['albumID']
            print album_id
            album = user.album_set.get(album_id=album_id)
            print album

            image_list = []
            for image in album.image_set.all():
                _dict = {}
                _dict['content'] = image.message
                print 'content ok '
                _dict['image'] = image.url
                print 'image ok'
                _dict['time'] = image.datetime
                print 'time ok'
                _dict['longitude'] = '东经：' + str(image.longitude) + '°'
                print 'longitude ok '
                _dict['latitude'] = '北纬：' + str(image.latitude) + '°'
                print 'latitude ok'
                image_list.append(_dict)
            print image_list
            return JsonResponse({'status': 'success', 'image': image_list})
        except:
            print 'no user reveal'
            return JsonResponse({'status': 'fail, no user reveal'})
    except:
        print 'no session got'
        return JsonResponse({'status': 'fail,but did not session got'})
