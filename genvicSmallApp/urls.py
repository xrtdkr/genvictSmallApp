"""genvicSmallApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'old_driver.views.wechat_login'),
    url(r'^upload/', 'old_driver.views.upload_init'),
    url(r'^fresh/', 'old_driver.views.refresh'),
    url(r'^newGroup/', 'old_driver.views.new_group'),
    url(r'^joinGroup/', 'old_driver.views.join_group'),
    url(r'^refresh/', 'old_driver.views.refresh'),
    url(r'^dismiss/', 'old_driver.views.dismiss'),
    url(r'^newPic/', 'old_driver.views.new_pic'),
]

