# -*- coding=utf-8 -*-

from django.contrib import auth

import logging
import os

from applications.common.services import *
from utils.check_auth import validate
from utils.check_obj import check_get_title, check_get_grade, check_get_clazz
from utils.const_err import *
from utils.const_def import *
from utils.net_helper import response200, response400, response_exception, response_parameter_error
from utils.utils_except import BusinessException
from utils.utils_log import log_exception


logger = logging.getLogger(__name__)


@validate('POST', auth=False)
def api_logout(request):
    auth.logout(request)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1]})


@validate('POST', auth=False)
def api_mobile_heartbeat(request):
    if not request.user.is_anonymous():
        request.session.modified = True
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1]})


@validate('GET', para=(
    {'name': 'key'},
))
def api_common_setting_detail(request, para):
    try:
        # if para['key'] != SETTING_KEY_REVIEW_YEAR:
        #     raise BusinessException(SETTING_KEY_WRONG)
        result = setting_detail(para['key'], request.user.school)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', para=(
    {'name': 'is_in', 'default': ''},
    {'name': 'title_id', 'default': '', 'convert': check_get_title},
    {'name': 'keyword', 'default': ''},
))
def api_common_teacher_list(request, para):
    # session_key = request.session.session_key
    # from django.contrib.sessions.models import Session
    # session = Session.objects.get(session_key=session_key)
    # data = session.get_decoded()
    # print data

    try:
        result = teacher_list(request.user.school, para['keyword'].strip(), para['is_in'], para['title'])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', para=(
    {'name': 'grade_id', 'default': '', 'convert': check_get_grade},
    {'name': 'clazz_id', 'default': '', 'convert': check_get_clazz},
    {'name': 'keyword', 'default': ''},
))
def api_common_student_list(request, para):
    try:
        grade_num = para['grade'].grade_num if para['grade'] else None
        result = student_list(request.user.school, para['keyword'], grade_num, para['clazz'])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET')
def api_common_class_list(request):
    try:
        result = class_list(request.user.school)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET')
def api_common_title_list(request):
    try:
        result = title_list(request.user.school)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})

