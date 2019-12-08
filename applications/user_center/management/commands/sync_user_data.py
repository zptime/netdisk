#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.core.management.base import BaseCommand
from ...sync import *
from django.conf import settings


class Command(BaseCommand):
    help = "this is a command customized for cleaning the database with a period of time(default is 7 days)!"
    default_time_period = 7

    def add_arguments(self, parser):
        parser.add_argument('--user_center', help="user center ip address.")
        parser.add_argument('--clean_all', action='store_true', help="clear all items")
        parser.add_argument('--clean_del_flag', action='store_true', help="clear all items del_flag=1")
        parser.add_argument('--ignore_update_time', action='store_true', help="sync data ignore update time")

    def handle(self, *args, **options):
        # 获取命令行参数
        clean_all = options['clean_all']
        clean_del_flag = options['clean_del_flag']
        ignore_update_time = options['ignore_update_time']
        user_center_ip = options['user_center']

        # 获取用户中心的domain
        if user_center_ip:
            uc_domain = "http://" + user_center_ip
        else:
            uc_domain = None

        # 删除所有表格中del_flag=True数据
        if clean_all or clean_del_flag:
            reversed_model_list = settings.MODEL_SYNC_FROM_USER_CENTER[:]
            reversed_model_list.reverse()
            for model_name in reversed_model_list:
                clear_table(model_name, clean_all)

        # 同步数据
        for model_name in settings.MODEL_SYNC_FROM_USER_CENTER:
            refresh_table(model_name, ignore_update_time, uc_domain)
