# 接口文档

### 接口文档模式
	## 事件：xxxxxxxx
	接口：xxxxxxxx
	接口注释：xxxxxxx	
	返回值：xxxxxx

## 1. 处理用户登录
	接口：url: www.ebichu.cn/login/
		  data: {code: xxx}
	方式: post
	{
		code: xxx,
	}
		  
	返回：{status: success/fail, sessionkey: xxx, }
	
	
## 1.5 处理用户上传的初始数据
	接口：url: www.ebichu.com/upload/
		data:{
			session: xxx,
			userInfo:
				{
	    			"nickName": "NICKNAME",
				    "gender": GENDER,
				    "city": "CITY",
				    "province": "PROVINCE",
				    "country": "COUNTRY",
				    "avatarUrl": "AVATARURL",
			    }

		}
		
	返回{status: success/fail}



## 2. 请求刷新用户数据(在创建了group以前进行刷新)
	注意带上session
	接口: www.ebichu.cn/fresh/
	方式: post
	data: {
		session: xxx,
		longtitude: xxxx,
		latitude: xxxx,
	}
	
	
	
	
## 3. 请求创建一个小组
	注意带上我所给的session
	接口： www.ebichu.cn/newGrowp/
	方式：post
	data:{
	
		***这里删除****
		groupID: xxxxx(五位整数),
		**************
		
		***这里添加****
		longitude: xxxx,
		latitude: xxxxx,
		*************
		
		session: xxxxx,
		
	}
	
	返回：{status: success(创建成功)/fail(创建失败), groupID:xxxxx}
	
	
## 4. 请求加入一个小组
	注意带上我所给的session
	接口： www.ebichu.cn/joinGroup/
	方式：post
	data:{
		groupID: xxxxx,
		session: xxx,
		
		***这里添加****
		longitude: xxxx,
		latitude: xxxxx,
		*************
	}
	返回：{status: success(加入成功)/fail(加入失败)}
	
	
## 7. 请求刷新用户数据(在创建了group以后进行刷新)
	注意带上session
	接口: www.ebichu.cn/refresh/
	方式: post
	data: {
		session: xxx,
		groupID: xxxxx,
		longtitude: xxxx,
		latitude: xxxx,
		state: xxxx,
	}
	
	返回：
	{
		isDismiss: False(表示没有解散)True(表示已经解散),
		
		user:
			[
				{
					nickname: xxx,
					iconurl: xxx,
					state: xxx,
					order: xxx,(用于显示那个0,1,2,3)
					isLeader: xxx,若isLeader是True,那么order一定是0,
					
					longitude:xxx,
					latitude:xxx,
				},
				...,
				{
					nickname: xxx,
					iconurl: xxx,
					state: xxx,
					order: xxx,(用于显示那个1，2，3)
					isLeader: xxx,若isLeader是True,那么order一定是1,
					
					longtitude:xxx,
					latitude:xxx,
				},
			],
			
			# 排序返回给前台。
	}
	
	
	
	
## 8.leader解散一个团队
	注意带上session
	接口: www.ebichu.cn/dismiss/
	方式: post
	data: {
		session: xxx,
		groupID: xxxxx,
	}
	返回: {status: success/fail}
	
## 9.退出一个团队(待定。)
	注意带上session
	接口: www.ebichu.cn/logout/
	方式: post
	data: {
		session: xxx,
		groupID: xxxxx,
	}
	返回: {status: success/fail, session: xxxx}
	
	
## 10.图片上传
<a href="https://mp.weixin.qq.com/debug/wxadoc/dev/api/network-file.html#wxuploadfileobject">参考文档</a>

	注意带上session
	接口：www.ebichu.cn/newPic/
	方式: post
	(使用微信服务器的上传模块)
	在from-data中额外添加以下字段：
	session: xxx,
	message: xxx,
	latitude: xxx,
	longitude: xxx,
	datetime: xxx,
	返回
	{"status": True}
	

## 11. 相册刷新

	注意带上session
	接口: www.ebichu.cn/refreshPic/
	
	{
		session:xxxx,
		image:[
			{
				url:xxx(服务器中的url),
				message:xxx,
				datetime:xxx,
				latitude:xxx,
				longitude:xxx,
			}
			...
			{
				url:xxx(服务器中的url),
				message:xxx,
				date:xxx,
				latitude:xxx,
				longitude:xxx,
			}
		]
	}	
	然后根据这份json加载大体框架，然后再根据下面的进行图片请求。
	
## 12. 图片文件请求(请求下来请劳烦您存储到本地)
<a href="https://mp.weixin.qq.com/debug/wxadoc/dev/api/network-file.html#wxdownloadfileobject">参考文档</a>
	
## 13. 生成一个ablum
	
	注意带上session
	
	{
		session:xxxx,
		from time
	}
	
	
## 14. 


图片社交：
	
