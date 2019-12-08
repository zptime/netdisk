# coding=utf-8
import json

from django.contrib import auth

import logging
import os

from django.http import HttpResponse

from applications.schooldisk import service
from utils.check_auth import validate
from utils.const_err import *
from utils.net_helper import response200, response_exception, response400, response403
from utils.utils_except import BusinessException
from utils.utils_log import log_exception
from utils.utils_time import str2datetime, str2dt_DATE_STD, str2dt_DAY_STD
from utils.utils_uuid import suuid

logger = logging.getLogger(__name__)


@validate('GET', auth=True)
def api_schooldisk_summary(request):
    # 查询用户网盘空间占用户情况
    try:
        result = service.api_schooldisk_summary(request.user)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'dir_name', 'default': ''},
    {'name': 'file_id', 'default': ''},
    {'name': 'admin_teacherid_list', 'default': ''},
    {'name': 'upload_teacherid_list', 'default': ''},
    {'name': 'list_teacherid_list', 'default': ''},
    {'name': 'download_teacherid_list', 'default': ''},
))
def api_schooldisk_adddir(request, para):
    # 新增文件夹
    try:
        result = service.api_schooldisk_adddir(request.user, para["dir_name"], para["file_id"], para["admin_teacherid_list"], para["upload_teacherid_list"], para["list_teacherid_list"], para["download_teacherid_list"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_name'},
    {'name': 'file_id'},
    {'name': 'admin_teacherid_list', 'default': ''},
    {'name': 'upload_teacherid_list', 'default': ''},
    {'name': 'list_teacherid_list', 'default': ''},
    {'name': 'download_teacherid_list', 'default': ''},
))
def api_schooldisk_moddir(request, para):
    # 修改文件夹/文件名称
    try:
        result = service.api_schooldisk_moddir(request.user, para["file_name"], para["file_id"], para["admin_teacherid_list"], para["upload_teacherid_list"], para["list_teacherid_list"], para["download_teacherid_list"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True, para=(
    {'name': 'file_id'},
))
def api_schooldisk_qrydir(request, para):
    # 查询文件夹名称
    try:
        result = service.api_schooldisk_qrydir(request.user, para["file_id"])
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
def api_schooldisk_filelist(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_schooldisk_filelist(request.user, para["file_id"], para["qry_child"], para["file_type"],
                                                 para["file_name_like"], para["file_name_exact"], para["size"], para["page"], para["last_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_id', 'default': ''},
    {'name': 'file_obj_id_list', 'default': ''},
    {'name': 'person_file_id_list', 'default': ''},
))
def api_schooldisk_submitfile(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_schooldisk_submitfile(request.user, para["file_id"], para["file_obj_id_list"], para["person_file_id_list"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_id_list', 'default': ''},
    {'name': 'file_id_del_all', 'default': ''},
))
def api_schooldisk_delfile(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_schooldisk_delfile(request.user, para["file_id_list"], para["file_id_del_all"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True, para=(
    {'name': 'file_id_list', 'default': ''},
    {'name': 'file_id_get_all', 'default': ''},
))
def api_schooldisk_getdownloadurl(request, para):
    # 获取文件列表中的下载地址
    try:
        result = service.api_schooldisk_getdownloadurl(request.user, para["file_id_list"], para["file_id_get_all"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'src_file_id_list', 'default': ''},
    {'name': 'desc_file_id', 'default': ''},
    {'name': 'file_id_move_all', 'default': ''},
))
def api_schooldisk_movfile(request, para):
    # 查询当前目录下所有文件夹/文件
    try:
        result = service.api_schooldisk_movfile(request.user, para["src_file_id_list"], para["desc_file_id"], para["file_id_move_all"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True)
def api_schooldisk_refreshspace(request):
    # 刷新当前用户的使用空间
    try:
        result = service.refresh_school_space(request.user.school)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True)
def api_schooldisk_getoatarget(request):
    """
        调用oa，获取oa的组织结构信息。
    """
    payload = {
        'account_id': request.user.id,
    }

    try:
        logger.info('proxy to oa:')
        logger.info(payload)
        remote_response = service.api_oa_send_target(payload)
    except Exception as e:
        logger.exception(e)
        return response200({'c': FAIL[0], 'm': FAIL[1], 'd': u'调用OA平台失败'})
    logger.info('oa return response:')
    logger.info(remote_response)
    return response200(remote_response)


@validate('POST', auth=True, para=(
    {'name': 'dir_file_id', 'default': ''},
))
def api_schooldisk_getuserdirrole(request, para):
    # 获取当前用户当前文件夹的权限，
    try:
        result = service.api_schooldisk_getuserdirrole(request.user, para["dir_file_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=True, para=(
    {'name': 'file_id', 'default': ''},
))
def api_schooldisk_getuserfilerole(request, para):
    # 获取当前用户当前文件的权限，
    try:
        result = service.api_schooldisk_getuserfilerole(request.user, para["file_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True, para=(
    {'name': 'dir_file_id', 'default': ''},
))
def api_schooldisk_dirstatistics(request, para):
    # 获取文件夹统计信息，
    try:
        result = service.api_schooldisk_dirstatistics(request.user, para["dir_file_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True, para=(
    {'name': 'startdate', 'default': ''},
    {'name': 'enddate', 'default': ''},
    {'name': 'dir_file_id', 'default': ''},
))
def api_schooldisk_dayuploadinfo(request, para):
    # 获取文件夹每日文件上传情况信息，
    try:
        result = service.api_schooldisk_dayuploadinfo(request.user, para["startdate"], para["enddate"], para["dir_file_id"])
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=True)
def api_schooldisk_alldirsummary(request):
    # 获取所有文件夹摘要信息，
    try:
        result = service.api_schooldisk_alldirsummary(request.user)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
