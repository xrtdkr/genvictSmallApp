from django.test import TestCase

# Create your tests here.

from old_driver.models import Group, WxUser

from django.conf import settings

settings.configure()

def clear_all_group_relationship():
    group = Group.objects.get(group_id='')
    for user in WxUser.objects.all():
        user.group = group
        user.save()


clear_all_group_relationship()
