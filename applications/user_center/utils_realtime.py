# -*- coding=utf-8 -*-

import json
import logging

from django.contrib.auth.hashers import get_hasher, identify_hasher
from django.db import connections
from django.conf import settings
from django.contrib import auth
from models import Account


logger = logging.getLogger(__name__)


def login_realtime(request, login_name, password):
    username = _get_username(login_name)
    if not username:
        return False
    if _check_user_validate(username, password):
        user = _get_user_by_username(username)
        if user and user.is_active:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return True
        else:
            return False
    return False


def get_password(mobile):
    sql = \
        u"select encoded_pwd from account where del_flag = '0' and mobile='%s'" % mobile
    cursor = connections['school_center'].cursor()
    cursor.execute(sql)
    queryset = cursor.fetchone()
    if queryset and len(queryset) > 0:
        passwd_encryped = queryset[0]
        return passwd_encryped
    else:
        return None


def _get_username(login_name):
    sql = \
        u"select username from account where del_flag = '0' and (username = '%s' or code='%s' or mobile='%s')" \
            % (login_name, login_name, login_name)
    cursor = connections['school_center'].cursor()
    cursor.execute(sql)
    queryset = cursor.fetchone()
    if queryset and len(queryset) > 0:
        return queryset[0]
    else:
        return None


def _check_user_validate(username, password):

    sql = u"select password from account where del_flag = '0' and username = '%s'" % username

    cursor = connections['school_center'].cursor()
    cursor.execute(sql)
    queryset = cursor.fetchone()

    if queryset and len(queryset) > 0:
        password_hashed = queryset[0]
        hasher = identify_hasher(password_hashed)
        return hasher.verify(password, password_hashed)
    else:
        return False


def get_clazz_id_by_teacher(teacher_id):
    sql = \
        u"select cls_id, is_master from teacher_class where del_flag = '0' and teacher_id = '%s'" % str(teacher_id)
    cursor = connections['school_center'].cursor()
    cursor.execute(sql)
    queryset = cursor.fetchall()
    result = list()
    if queryset:
        for each in queryset:
            result.append({
                'clazz_id': int(each[0]),
                'is_mentor': int(each[1])
            })
    return result


def _get_user_by_username(username):
    return Account.objects.filter(username=username, del_flag=0).first()