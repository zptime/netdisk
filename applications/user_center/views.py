#!/usr/bin/python
# -*- coding=utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth import logout
from django_cas_ng import views as cas_views
import agents
from utils import *
import json
import traceback
import logging
import sync

logger = logging.getLogger(__name__)


def api_login(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if settings.USE_USER_CENTER_DB_LOGIN:  # 使用用户中心数据库
            from utils_realtime import login_realtime
            if login_realtime(request, username, password):
                dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1]}
            else:
                dict_resp = {"c": ERR_LOGIN_FAIL[0], "m": ERR_LOGIN_FAIL[1]}
        else:  # 使用本地数据库
            if agents.login(request, username, password):
                dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1]}
            else:
                dict_resp = {"c": ERR_LOGIN_FAIL[0], "m": ERR_LOGIN_FAIL[1]}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_logout(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        cas_views.callback(request)
        dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1]}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_call_api(request, api_name):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        resp_data = agents.call_api(request, api_name)
        return HttpResponse(resp_data, content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_service_apps(request):
    return api_call_api(request, "api_list_service_apps")


def api_detail_account(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        username = request.POST.get('username', "")
        dict_resp = agents.api_detail_account(request.user)  # 首先查询本地数据库，然后查询用户中心
        if dict_resp["d"]:
            return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
        else:
            return api_call_api(request, "api_detail_account")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_reset_password(request):
    return api_call_api(request, 'api_reset_password')


def api_list_user_type(request):
    return api_call_api(request, 'api_list_user_type')


def api_change_user_type(request):
    return api_call_api(request, 'api_change_user_type')


def api_school_list_subject(request):
    return api_call_api(request, 'api_school_list_subject')


def api_upload_image(request):
    return api_call_api(request, 'api_upload_image')


def api_update_teacher(request):
    return api_call_api(request, 'api_update_teacher')


def api_update_parent(request):
    return api_call_api(request, 'api_update_parent')


def api_update_student(request):
    return api_call_api(request, 'api_update_student')


def api_list_grade(request):
    return api_call_api(request, 'api_list_grade')


def api_list_class(request):
    return api_call_api(request, 'api_list_class')


def api_school_list_textbook(request):
    return api_call_api(request, 'api_school_list_textbook')


def api_list_teacher_textbook(request):
    return api_call_api(request, 'api_list_teacher_textbook')


def api_update_teacher_textbook(request):
    return api_call_api(request, 'api_update_teacher_textbook')


def api_add_teacher_textbook(request):
    return api_call_api(request, 'api_add_teacher_textbook')


def api_delete_teacher_textbook(request):
    return api_call_api(request, 'api_delete_teacher_textbook')


def api_list_teacher_class(request):
    return api_call_api(request, 'api_list_teacher_class')


def api_delete_teacher_class(request):
    return api_call_api(request, 'api_delete_teacher_class')


def api_add_teacher_class(request):
    return api_call_api(request, 'api_add_teacher_class')


def api_get_user_center_url(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        internet_url = agents.get_user_center_url()
        resp_data = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": [internet_url]}
        return HttpResponse(json.dumps(resp_data), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


@internal_or_403
def api_refresh_item(request):
    dict_resp = auth_check(request, "POST", check_login=False)
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    try:
        model_name = request.POST["model_name"]
        item_id = request.POST["item_id"]
        item_data = request.POST["item_data"]
        resp_data = sync.refresh_item(model_name, item_id, item_data)
        return HttpResponse(json.dumps(resp_data), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


# ----------------------------------------------------------------
# api added in teacher_resources, and communicate with user center
def api_list_teacher_textbook_local(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        teacher_id = request.POST.get("teacher_id", "")
        subject_id = request.POST.get("subject_id", "")
        dict_resp = agents.list_teacher_textbook(request.user, teacher_id, subject_id)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_school_textbook(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        subject_id_list = request.POST.get("subject_id_list", [])
        if subject_id_list:
            subject_id_list = json.loads(subject_id_list)
        grade_num_list = request.POST.get("grade_num_list", [])
        if grade_num_list:
            grade_num_list = json.loads(grade_num_list)
        dict_resp = agents.school_list_textbook(user=request.user, subject_id_list=subject_id_list, grade_num_list=grade_num_list)
        if dict_resp["d"]:
            return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
        else:
            return api_call_api(request, "api_school_list_textbook")

    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = dict(c=-1, m=ex.message)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_chapter(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        textbook_id = request.POST.get("textbook_id", "")

        dict_resp = agents.admin_list_chapter(user=request.user, textbook_id=textbook_id)
        if dict_resp["d"]:
            return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
        else:
            return api_call_api(request, "api_admin_list_chapter")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_subject(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = agents.school_list_subject(user=request.user)
        if dict_resp["d"]:
            return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
        else:
            return api_call_api(request, "api_school_list_subject")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def api_list_title(request):
    dict_resp = auth_check(request, "POST")
    if dict_resp != {}:
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    try:
        dict_resp = agents.list_title(request.user)
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")
    except Exception as ex:
        sErrInfo = traceback.format_exc()
        logger.error(sErrInfo)
        dict_resp = {"c": -1, "m": ex.message}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")