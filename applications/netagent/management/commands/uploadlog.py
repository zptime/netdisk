# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from django.db import models
# from placeholders import *
import os

from applications.netagent.netrequest import *
from applications.netagent.report import daily_report
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    def handle(self, *args, **options):
        daily_report()
        # sendemail(None, 'liukai5481@fiberhome.com', u'邮件后台发送测试', u'邮件正文测试')
        # sendemail('C:\Users\liukai\Desktop\desktop.ini', 'liukai5481@fiberhome.com', u'邮件后台发送测试', u'邮件正文测试')
        # get_url('http://test-evaluate.hbeducloud.com:88/user_center/api/login', 'POST', '{"username":"fenghuo","password":"fh123456"}', '')
