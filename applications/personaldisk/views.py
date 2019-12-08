# coding=utf-8

from django.contrib import auth

import logging
import os

from django.http import HttpResponse


from applications.personaldisk import service
from utils.check_auth import validate, is_admin
from utils.const_err import *
from utils.net_helper import response200, response_exception, response400, response403
from utils.utils_except import BusinessException
from utils.utils_log import log_exception
from utils.utils_time import str2datetime, str2dt_DATE_STD, str2dt_DAY_STD
from utils.utils_uuid import suuid

logger = logging.getLogger(__name__)


@validate('GET', auth=False, para=(
    {'name': 'type', 'default': '0'},   # 测试
))
def api_test(request, para):
    try:
        if para['type'] != '1':
            result = service.api_test(request.user, para['type'])
        else:
            raise BusinessException(FAIL)

    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True)
def api_persondisk_summary(request):
    # 查询用户网盘空间占用户情况
    try:
        result = service.api_persondisk_summary(request.user)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'dir_name', 'default': ''},
    {'name': 'file_id', 'default': ''},
))
def api_persondisk_adddir(request, para):
    # 新增文件夹
    try:
        result = service.api_persondisk_adddir(request.user, para["dir_name"], para["file_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_name'},
    {'name': 'file_id'},
))
def api_persondisk_modname(request, para):
    # 修改文件夹/文件名称
    try:
        result = service.api_persondisk_modname(request.user, para["file_name"], para["file_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True, para=(
    {'name': 'file_id', 'default': ''},
    {'name': 'qry_child', 'default': ''},
    {'name': 'file_type', 'default': ''},
    {'name': 'file_name_exact', 'default': ''},
    {'name': 'file_name_like', 'default': ''},
    {'name': 'size', 'default': ''},
    {'name': 'page', 'default': ''},
    {'name': 'last_id', 'default': ''},  # 暂不支持
))
def api_persondisk_filelist(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_persondisk_filelist(request.user, para["file_id"], para["qry_child"], para["file_type"],
                                                 para["file_name_like"], para["file_name_exact"], para["size"], para["page"], para["last_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_id', 'default': ''},
    {'name': 'file_obj_id_list', 'default': ''},
))
def api_persondisk_submitfile(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_persondisk_submitfile(request.user, para["file_id"], para["file_obj_id_list"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_id_list', 'default': ''},
    {'name': 'file_id_del_all', 'default': ''},
))
def api_persondisk_delfile(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_persondisk_delfile(request.user, para["file_id_list"], para["file_id_del_all"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True, para=(
    {'name': 'file_id_list', 'default': ''},
    {'name': 'file_id_get_all', 'default': ''},
))
def api_persondisk_getdownloadurl(request, para):
    # 获取文件列表中的下载地址
    try:
        result = service.api_persondisk_getdownloadurl(request.user, para["file_id_list"], para["file_id_get_all"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'src_file_id_list', 'default': ''},
    {'name': 'desc_file_id', 'default': ''},
    {'name': 'file_id_move_all', 'default': ''},
))
def api_persondisk_movfile(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_persondisk_movfile(request.user, para["src_file_id_list"], para["desc_file_id"], para["file_id_move_all"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True)
def api_persondisk_refreshspace(request):
    # 刷新当前用户的使用空间
    try:
        result = service.refresh_user_space(request.user)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


#@validate('GET', auth=True, para=(
#    {'name': 'tk', 'default': ''},
#))
def api_persondisk_checkauth(request, file_name=''):
    # 刷新当前用户的使用空间
    try:
        # request_str = (str(request.GET.items())).replace("u\'", "\'").decode('unicode-escape').encode('utf8')
        logger.info(file_name)
        # logger.info(request_str)
        # logger.info(request.get_full_path())
        tk = request.GET.get('tk', '')
        logger.info(tk)
        result = service.api_persondisk_checkauth(request.user, file_name, tk)

    except Exception as e:
        log_exception(e)
        return response403(u'无访问权限')
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


