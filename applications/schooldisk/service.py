# -*- coding=utf-8 -*-
import json
import datetime
from urlparse import urljoin, urlparse

import requests
from django.db import transaction
from django.db.models import Sum

from applications.common.services import setting_detail
from applications.personaldisk.models import NetdiskPersonalFile
from applications.schooldisk.models import NetdiskSchoolSize, NetdiskSchoolFile, NetdiskSchoolRole
from applications.personaldisk.service import get_friendly_size
from applications.upload_resumable.models import FileObj
from applications.user_center.models import Service, Teacher
from utils.check_auth import is_admin_by_user
from utils.const_def import *
from utils.const_err import *
from utils.net_helper import url_with_uc_domain
from utils.utils_except import BusinessException
from utils.utils_time import today, get_day_list, get_day_cycle, datetime2str, str2datetime
from utils.utils_tools import get_pages, AES_Obj
import logging
logger = logging.getLogger(__name__)


def api_schooldisk_summary(user):
    school_total_size_b = setting_detail("SCHOOL_MAX_SIZE", user.school)["value"]
    school_size = NetdiskSchoolSize.objects.filter(school=user.school, is_del=FALSE_INT).first()

    if school_size:
        school_used_size_b = str(school_size.totalsize)
    else:
        school_used_size_b = "0"

    school_total_size = get_friendly_size(school_total_size_b)
    school_used_size = get_friendly_size(school_used_size_b)

    result = {
        "school_total_size_b": school_total_size_b,
        "school_used_size_b": school_used_size_b,
        "school_total_size": school_total_size,
        "school_used_size": school_used_size,
    }
    return result


@transaction.atomic
def api_schooldisk_adddir(user, dir_name, file_id, admin_teacherid_list, upload_teacherid_list, list_teacherid_list, download_teacherid_list):
    admin_teacherid_list = json.loads(admin_teacherid_list) if admin_teacherid_list else []
    upload_teacherid_list = json.loads(upload_teacherid_list) if upload_teacherid_list else []
    list_teacherid_list = json.loads(list_teacherid_list) if list_teacherid_list else []
    download_teacherid_list = json.loads(download_teacherid_list) if download_teacherid_list else []

    # 检查是否有创建文件夹权限，只有管理员权限可以创建文件夹
    cur_user_dir_role = api_schooldisk_getuserdirrole(user, file_id)
    if len(set(ROLE_ADMIN) & set(cur_user_dir_role)) == 0:
        raise BusinessException(NETDISK_ERR_NO_ROLE_MKDIR)

    # 文件名不能为空
    if not dir_name:
        raise BusinessException(NETDISK_ERR_FILENAME)

    # 检查上级文件夹是否存在, 检查是否存在同名的文件夹。
    if file_id:
        cur_dir = NetdiskSchoolFile.objects.filter(id=file_id, school=user.school, is_del=FALSE_INT).first()
        if not cur_dir:
            raise BusinessException(NETDISK_ERR_NULL_DIR)
        file_same_names = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, name=dir_name, is_dir=TRUE_INT, parent_id=file_id)
    else:
        file_same_names = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, name=dir_name, is_dir=TRUE_INT, parent_id=None)

    if file_same_names:
        raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

    # 增加文件夹
    netdiskschoolalfile = NetdiskSchoolFile()
    netdiskschoolalfile.school = user.school
    netdiskschoolalfile.account = user
    netdiskschoolalfile.name = dir_name
    netdiskschoolalfile.is_dir = TRUE_INT
    netdiskschoolalfile.fileobj = None
    netdiskschoolalfile.parent_id = file_id if file_id else None
    netdiskschoolalfile.save()

    result = {
        "file_id": netdiskschoolalfile.id,
    }

    # 增加相应的权限信息
    dir_mod_teacher_role(netdiskschoolalfile.id, admin_teacherid_list, ROLE_TYPE_ADMIN)
    dir_mod_teacher_role(netdiskschoolalfile.id, upload_teacherid_list, ROLE_TYPE_UPLOAD)
    dir_mod_teacher_role(netdiskschoolalfile.id, list_teacherid_list, ROLE_TYPE_LIST)
    dir_mod_teacher_role(netdiskschoolalfile.id, download_teacherid_list, ROLE_TYPE_DOWNLOAD)

    return result


def dir_mod_teacher_role(dir_file_id, teacher_id_list, role_type):
    """
    为文件夹添加老师权限，全量修改，会删除所有旧的权限，添加新的权限。
    :param dir_file_id: 文件夹id
    :param teacher_id_list:  老师id
    :param role_type:   权限类型
    :return:
    """
    # 由于前端每次都全量传过来，因此先删除原权限，然后添加新权限
    NetdiskSchoolRole.objects.filter(netdiskschoolfile_id=dir_file_id, role_type=role_type).update(is_del=TRUE_INT)

    # 增加全体老师
    if 'all_teacher' in teacher_id_list:
        netdiskschoolrole, created = NetdiskSchoolRole.objects.update_or_create(netdiskschoolfile_id=dir_file_id,
                                                                                account=None,
                                                                                role_type=role_type,
                                                                                teacher=None,
                                                                                defaults={'is_del': FALSE_INT})
        return

    for each_teacher_id in teacher_id_list:
        # 检查老师是否存在
        teacher = Teacher.objects.filter(id=each_teacher_id, del_flag=FALSE_INT).first()
        if not teacher:
            logger.error(u"待添加的老师id不存在，id：%s" % each_teacher_id)
            raise BusinessException(TEACHER_NOT_EXIST)

        netdiskschoolrole, created = NetdiskSchoolRole.objects.update_or_create(netdiskschoolfile_id=dir_file_id,
                                                                                account=teacher.account,
                                                                                role_type=role_type,
                                                                                teacher=teacher,
                                                                                defaults={'is_del': FALSE_INT})
        # netdiskschoolrole = NetdiskSchoolRole()
        # netdiskschoolrole.netdiskschoolfile_id = dir_file_id
        # netdiskschoolrole.account = teacher.account
        # netdiskschoolrole.role_type = role_type
        # netdiskschoolrole.teacher = teacher
        # netdiskschoolrole.save()
    return


def api_schooldisk_moddir(user, file_name, file_id, admin_teacherid_list, upload_teacherid_list, list_teacherid_list, download_teacherid_list):
    admin_teacherid_list = json.loads(admin_teacherid_list) if admin_teacherid_list else []
    upload_teacherid_list = json.loads(upload_teacherid_list) if upload_teacherid_list else []
    list_teacherid_list = json.loads(list_teacherid_list) if list_teacherid_list else []
    download_teacherid_list = json.loads(download_teacherid_list) if download_teacherid_list else []

    # 文件名不能为空
    if not file_name:
        raise BusinessException(NETDISK_ERR_FILENAME)
    if not file_id:
        raise BusinessException(REQUEST_PARAM_ERROR)

    # if not is_myfile(user.id, [file_id]):
    #     raise BusinessException(NETDISK_ERR_NOPERMISSION)

    # 检查文件是否存在，检查是否有新的同名文件夹
    cur_file = NetdiskSchoolFile.objects.filter(id=file_id, school=user.school, is_del=FALSE_INT).first()
    if not cur_file:
        raise BusinessException(NETDISK_ERR_NULL_DIR)
    file_same_names = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, name=file_name, is_dir=TRUE_INT,
                                                       parent_id=cur_file.parent_id).exclude(id=file_id)
    if file_same_names:
        raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

    # 检查是否有上级目录修改权限,即上级目录的管理员权限。
    cur_user_dir_role = api_schooldisk_getuserdirrole(user, cur_file.parent_id)
    if len(set(ROLE_ADMIN) & set(cur_user_dir_role)) == 0:
        raise BusinessException(NETDISK_ERR_NOPERMISSION)

    cur_file.name = file_name
    cur_file.save()

    result = {
        "file_id": cur_file.id,
        "file_name": cur_file.name,
    }

    # 增加相应的权限信息
    dir_mod_teacher_role(cur_file.id, admin_teacherid_list, ROLE_TYPE_ADMIN)
    dir_mod_teacher_role(cur_file.id, upload_teacherid_list, ROLE_TYPE_UPLOAD)
    dir_mod_teacher_role(cur_file.id, list_teacherid_list, ROLE_TYPE_LIST)
    dir_mod_teacher_role(cur_file.id, download_teacherid_list, ROLE_TYPE_DOWNLOAD)

    return result


def api_schooldisk_qrydir(user, file_id):
    result = dict()
    if not file_id:
        raise BusinessException(NETDISK_ERR_NOT_SUPPORT_ROOTQRY)

    dir_file = NetdiskSchoolFile.objects.filter(school=user.school, id=file_id, is_dir=TRUE_INT, is_del=FALSE_INT).first()
    if not dir_file:
        raise BusinessException(NETDISK_ERR_NULL_DIR)

    result['dir_name'] = dir_file.name
    result['admin_teacherid_list'] = get_dir_role_teachers(dir_file, ROLE_TYPE_ADMIN)
    result['upload_teacherid_list'] = get_dir_role_teachers(dir_file, ROLE_TYPE_UPLOAD)
    result['list_teacherid_list'] = get_dir_role_teachers(dir_file, ROLE_TYPE_LIST)
    result['download_teacherid_list'] = get_dir_role_teachers(dir_file, ROLE_TYPE_DOWNLOAD)

    return result


def get_dir_role_teachers(dir_file, role_type):
    """
    获取某个文件夹某种权限的所有老师信息
    :param dir_file:
    :param role_type:
    :return:
    """
    result = list()
    role_teachers = NetdiskSchoolRole.objects.filter(netdiskschoolfile=dir_file, role_type=role_type, is_del=FALSE_INT)
    for each_role in role_teachers:
        if not each_role.teacher:
            return ['all_teacher']

        if each_role.teacher and each_role.teacher.del_flag == TRUE_INT:
            continue

        teacher_dict = dict()
        teacher_dict['teacher_id'] = each_role.teacher_id
        teacher_dict['account_id'] = each_role.teacher.account_id
        teacher_dict['teacher_name'] = each_role.teacher.full_name
        teacher_dict['image_url'] = url_with_uc_domain(each_role.teacher.image_url) if each_role.teacher.image_url else ''
        result.append(teacher_dict)
    return result


def is_myfile(account_id, file_id_list):
    # 检查是不是我的网盘文件
    file_id_list = list(set(file_id_list))  # 去重
    netdiskfilecnt = NetdiskSchoolFile.objects.filter(account_id=account_id, id__in=file_id_list, is_del=FALSE_INT).count()
    return True if netdiskfilecnt >= len(file_id_list) else False


@transaction.atomic
def api_schooldisk_submitfile(user, file_id, file_obj_id_list, person_file_id_list):
    file_obj_id_list = json.loads(file_obj_id_list) if file_obj_id_list else []
    person_file_id_list = json.loads(person_file_id_list) if person_file_id_list else []

    if not file_id:
        raise BusinessException(NETDISK_ERR_ROOT_NOFILE)

    # 检查目标文件夹是否存在
    cur_file = NetdiskSchoolFile.objects.filter(id=file_id, is_dir=TRUE_INT, school=user.school, is_del=FALSE_INT).first()
    if not cur_file:
        raise BusinessException(NETDISK_ERR_NULL_DIR)

    totalspace = 0
    parent_id = file_id if file_id else None

    # 提交上传的文件
    for each_fileid in file_obj_id_list:
        # 检查文件是否存在
        fileobj = FileObj.objects.filter(id=each_fileid, del_flag=FALSE_INT).first()
        if not fileobj:
            raise BusinessException(NETDISK_ERR_NO_FILEOBJ)

        # 检查是否有同名的文件
        file_same_names = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, name=fileobj.name, is_dir=FALSE_INT,
                                                           parent_id=parent_id)
        if not file_id:
            # file_same_names = file_same_names.filter(parent_id=file_id)
            raise BusinessException(NETDISK_ERR_ROOT_NOFILE)

        if file_same_names:
            raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

        netdiskschoolalfile = NetdiskSchoolFile()
        netdiskschoolalfile.school = user.school
        netdiskschoolalfile.account = user
        netdiskschoolalfile.name = fileobj.name
        netdiskschoolalfile.is_dir = FALSE_INT
        netdiskschoolalfile.fileobj = fileobj
        netdiskschoolalfile.parent_id = parent_id
        netdiskschoolalfile.save()

        totalspace = totalspace + fileobj.size

    # 提交个人网盘的文件
    for each_fileid in person_file_id_list:
        # 检查文件是否存在
        person_file = NetdiskPersonalFile.objects.filter(id=each_fileid, is_del=FALSE_INT).first()
        if not person_file:
            raise BusinessException(NETDISK_ERR_NO_PERSONFILE)

        # 检查是否有同名的文件
        file_same_names = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, name=person_file.name, is_dir=FALSE_INT,
                                                           parent_id=parent_id)
        if file_id:
            file_same_names = file_same_names.filter(parent_id=file_id)

        if file_same_names:
            logger.error(u'存在同名文件%s' % person_file.name)
            raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

        netdiskschoolalfile = NetdiskSchoolFile()
        netdiskschoolalfile.school = user.school
        netdiskschoolalfile.account = user
        netdiskschoolalfile.name = person_file.name
        netdiskschoolalfile.is_dir = FALSE_INT
        netdiskschoolalfile.fileobj = person_file.fileobj
        netdiskschoolalfile.parent_id = parent_id
        netdiskschoolalfile.save()

        totalspace = totalspace + person_file.fileobj.size

    # 刷新使用空间, 以后如果文件传多了，就采用下面方式更新空间大小。
    # school_total_size_b = api_schooldisk_summary(user)['school_total_size_b']
    # school_used_size_b = api_schooldisk_summary(user)['school_used_size_b']
    #
    # if totalspace > school_total_size_b - school_used_size_b:
    #     raise BusinessException(NETDISK_ERR_SPACE_NOENOUPH)
    if not refresh_school_space(user.school):
        raise BusinessException(NETDISK_ERR_SPACE_NOENOUPH)
    return 'ok'


def api_schooldisk_filelist(user, file_id, qry_child, file_type, file_name_like, file_name_exact, size, page, last_id):
    # 查询文件列表
    result = dict()
    parent_id = file_id if file_id else None
    if parent_id:
        parent_file = NetdiskSchoolFile.objects.filter(school=user.school, id=parent_id, is_del=FALSE_INT).first()
        result['id'] = parent_file.id
        result['pid'] = parent_file.parent_id if parent_file.parent_id else 1
        result['filename'] = parent_file.name
        result['sizeb'] = parent_file.fileobj.size if parent_file.fileobj else ''
        result['size'] = get_friendly_size(result['sizeb']) if result['sizeb'] else ''
        result['is_dir'] = parent_file.is_dir
        result['update_time'] = parent_file.update_time.strftime(DEFAULT_FORMAT_DATETIME)
    else:
        result['id'] = 1
        result['pid'] = 0
        result['filename'] = '根目录'
        result['sizeb'] = ''
        result['size'] = ''
        result['is_dir'] = '1'
        result['update_time'] = ''

    file_list = get_child(user, file_id, qry_child, file_type, file_name_like, file_name_exact)

    # 分页
    cnt = len(file_list)
    num_pages = 1
    if size and page:
        num_pages, cur_start, cur_end = get_pages(cnt, page, size)
        file_list = file_list[cur_start:cur_end]
    elif size:
        cur_start = get_lastid_index(file_list, last_id)
        file_list = file_list[cur_start:cur_start+int(size)]
        pass

    result['file_list'] = file_list
    result["max_page"] = num_pages
    result["total"] = cnt

    return result


def get_lastid_index(file_list, last_id):
    index = 0
    last_id = int(last_id)
    for each_file in file_list:
        index += 1
        if each_file['id'] == last_id:
            return index

    return 0


def get_child(user, file_id, qry_child, file_type, file_name_like, file_name_exact):
    """
    递归查询目录下所有文件
    :param result:
    :param user: 当前用户
    :param file_id: 查询的目录id，如果是根目录，则
    :param qry_child: 是否包含下级
    :param file_type: 不传或传空查询全部，传1仅查询文件夹，传2仅查询文件
    :param file_name_like: 根据文件名模糊查询
    :param file_name_exact: 根据文件名精确查询
    :return:
    """
    child_list = list()
    parent_id = file_id if file_id else None

    netdiskfiles = NetdiskSchoolFile.objects.filter(school=user.school, parent_id=parent_id, is_del=FALSE_INT)
    if file_type == 1 or file_type == "1":
        netdiskfiles = netdiskfiles.filter(is_dir=TRUE_INT)
    elif file_type == 2 or file_type == "2":
        netdiskfiles = netdiskfiles.filter(is_dir=FALSE_INT)

    if file_name_like:
        netdiskfiles = netdiskfiles.filter(name__contains=file_name_like)

    if file_name_exact:
        netdiskfiles = netdiskfiles.filter(name=file_name_exact)

    netdiskfiles = netdiskfiles.order_by('-is_dir', '-update_time')
    for each_file in netdiskfiles:
        # 如果是目录，需要检查该用户在该目录有没有查看列表权限
        # 如果是文件，需要检查该用户在该文件所在目录有没有列表权限。
        if each_file.is_dir:
            cur_user_dir_role = api_schooldisk_getuserdirrole(user, each_file.id)
        else:
            cur_user_dir_role = api_schooldisk_getuserdirrole(user, each_file.parent_id)
        if len(set(ROLE_LIST) & set(cur_user_dir_role)) == 0:
            continue

        child = dict()
        child['id'] = each_file.id
        child['pid'] = each_file.parent_id if each_file.parent_id else 1  # 父节点ID，前端要求根节点必须为1
        child['filename'] = each_file.name
        child['sizeb'] = each_file.fileobj.size if each_file.fileobj else ''
        child['size'] = get_friendly_size(child['sizeb']) if child['sizeb'] else ''
        child['is_dir'] = each_file.is_dir
        child['update_time'] = each_file.update_time.strftime(DEFAULT_FORMAT_DATETIME)
        child_list.append(child)

        if qry_child == "1" or qry_child == 1:
            child['file_list'] = get_child(user, each_file.id, qry_child, file_type, file_name_like, file_name_exact)

    result = child_list

    return result


def get_childid_flat(user, file_id, qry_child, file_type, file_name_like, file_name_exact):
    """
    递归查询目录下所有文件id，以flat数组形式返回
    :param result:
    :param user: 当前用户
    :param file_id: 查询的目录id，如果是根目录，则
    :param qry_child: 是否包含下级
    :param file_type: 不传或传空查询全部，传1仅查询文件夹，传2仅查询文件
    :param file_name_like: 根据文件名模糊查询
    :param file_name_exact: 根据文件名精确查询
    :return:
    """
    child_list = list()
    parent_id = file_id if file_id else None

    netdiskfiles = NetdiskSchoolFile.objects.filter(school=user.school, parent_id=parent_id, is_del=FALSE_INT)
    if file_type == 1 or file_type == "1":
        netdiskfiles = netdiskfiles.filter(is_dir=TRUE_INT)
    elif file_type == 2 or file_type == "2":
        netdiskfiles = netdiskfiles.filter(is_dir=FALSE_INT)

    if file_name_like:
        netdiskfiles = netdiskfiles.filter(name__contains=file_name_like)

    if file_name_exact:
        netdiskfiles = netdiskfiles.filter(name=file_name_exact)

    netdiskfiles = netdiskfiles.order_by('-is_dir', '-update_time')
    for each_file in netdiskfiles:
        child_list.append(each_file.id)

        if qry_child == "1" or qry_child == 1 or qry_child == True:
            grandson = get_childid_flat(user, each_file.id, qry_child, file_type, file_name_like, file_name_exact)
            child_list.extend(grandson)

    result = child_list

    return result


@transaction.atomic
def api_schooldisk_delfile(user, file_id_list, file_id_del_all):
    if file_id_list:
        file_id_list = json.loads(file_id_list)
    elif file_id_del_all:
        file_id_list = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, parent_id=file_id_del_all).values_list('id', flat=True)
    else:
        file_id_list = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, parent_id=None).values_list('id', flat=True)

    file_id_list = list(file_id_list)
    if len(file_id_list) == 0:
        raise BusinessException(NETDISK_ERR_NO_DEL_FILE)

    # 检查文件是否在同一目录，暂不支持不同目录的文件同时删除(实际原因是不大可能出现此情况，所以懒得写这个代码去支持了^_^!!)。
    parent_file = NetdiskSchoolFile.objects.filter(school=user.school, id__in=list(file_id_list), is_del=FALSE_INT).values('parent_id').distinct()
    if parent_file.count() > 1:
        raise BusinessException(NETDISK_ERR_FILE_NOTIN_SAMEDIR)
    if parent_file.count() == 0:
        raise BusinessException(NETDISK_ERR_NO_FILEOBJ)

    # 检查我是否是管理员，只有管理员和自己可以删除文件
    cur_user_dir_role = api_schooldisk_getuserdirrole(user, parent_file.first()['parent_id'])
    if len(set(ROLE_ADMIN) & set(cur_user_dir_role)) == 0:
        # 检查是否是我的文件
        if not is_myfile(user.id, file_id_list):
            raise BusinessException(NETDISK_ERR_NOPERMISSION)
        # raise BusinessException(NETDISK_ERR_NO_ROLE_MKDIR)

    del_fileid_list = list()
    for each_file_id in file_id_list:
        del_fileid_list.append(each_file_id)
        del_fileid_list.extend(get_childid_flat(user, file_id=each_file_id, qry_child=1, file_type=None, file_name_like=None, file_name_exact=None))

    # 删除文件/文件夹，同时删除文件夹权限
    NetdiskSchoolFile.objects.filter(school=user.school, id__in=list(del_fileid_list)).update(is_del=TRUE_INT)
    NetdiskSchoolRole.objects.filter(netdiskschoolfile__in=list(del_fileid_list)).update(is_del=TRUE_INT)

    refresh_school_space(user.school)

    return 'ok'


@transaction.atomic
def api_schooldisk_movfile(user, src_file_id_list, desc_file_id, file_id_move_all):
    if src_file_id_list:
        src_file_id_list = json.loads(src_file_id_list)
    elif file_id_move_all:
        src_file_id_list = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, parent_id=file_id_move_all).values_list('id', flat=True)
    else:
        src_file_id_list = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, parent_id=None).values_list('id', flat=True)

    src_file_id_list = list(src_file_id_list)
    # 检查文件是否在同一目录，暂不支持不同目录的文件同时移动(实际原因是不大可能出现此情况，所以懒得写这个代码去支持了^_^!!)。
    src_parent_file = NetdiskSchoolFile.objects.filter(school=user.school, id__in=list(src_file_id_list), is_del=FALSE_INT).values('parent_id').distinct()
    if src_parent_file.count() > 1:
        raise BusinessException(NETDISK_ERR_FILE_NOTIN_SAMEDIR)

    # 检查我是否是管理员，只有管理员和自己可以把文件移走即删除
    cur_user_src_dir_role = api_schooldisk_getuserdirrole(user, src_parent_file.first()['parent_id'])
    if len(set(ROLE_ADMIN) & set(cur_user_src_dir_role)) == 0:
        # 检查是否是我的文件
        if not is_myfile(user.id, src_file_id_list):
            raise BusinessException(NETDISK_ERR_NOPERMISSION)
        # raise BusinessException(NETDISK_ERR_NO_ROLE_MKDIR)

    # 检查目标文件夹我是否具有上传权限
    cur_user_desc_dir_role = api_schooldisk_getuserdirrole(user, desc_file_id)
    if len(set(ROLE_UPLOAD) & set(cur_user_desc_dir_role)) == 0:
        # 检查是否有上传文件权限（注意此处仍保留了文件原来的上传人信息）
        raise BusinessException(NETDISK_ERR_NOPERMISSION)
        # raise BusinessException(NETDISK_ERR_NO_ROLE_MKDIR)

    # 如果是根目录，还需要检查要移动的是否全部是文件夹，因为根目录不能存放文件。
    if not desc_file_id:
        src_is_not_dir = NetdiskSchoolFile.objects.filter(school=user.school, id__in=src_file_id_list, is_del=FALSE_INT, is_dir=FALSE_INT)
        if src_is_not_dir:
            raise BusinessException(NETDISK_ERR_ROOT_NOFILE)

    # 没传目标文件夹就放到根目录去。
    if not desc_file_id:
        desc_file_id = None

    NetdiskSchoolFile.objects.filter(school=user.school, id__in=list(src_file_id_list), is_del=FALSE_INT).update(parent_id=desc_file_id)

    return 'ok'


def refresh_school_space(school):
    # usedspace = NetdiskSchoolFile.objects.filter(account=user, is_del=FALSE_INT, is_dir=FALSE_INT).values('fileobj.size') \
    #     .aggregate(totalspace=Sum('fileobj.size'))['totalspace']

    usedspace = FileObj.objects.filter(schoolfileobj__school=school, schoolfileobj__is_del=FALSE_INT, schoolfileobj__is_dir=FALSE_INT) \
        .aggregate(totalspace=Sum('size'))['totalspace']
    if not usedspace:
        usedspace = 0

    # 获取总空间
    totalspace = setting_detail('SCHOOL_MAX_SIZE', school)

    if usedspace > totalspace:
        return False
    netdiskpsize, created = NetdiskSchoolSize.objects.update_or_create(school=school,
                                                                       defaults={'is_del': FALSE_INT, 'totalsize': usedspace})
    return True


def api_schooldisk_getdownloadurl(user, file_id_list, file_id_get_all):
    result = dict()
    if file_id_list:
        file_id_list = json.loads(file_id_list)
    elif file_id_get_all:
        file_id_list = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, parent_id=file_id_get_all).values_list('id', flat=True)
    else:
        file_id_list = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, parent_id=None).values_list('id', flat=True)

    if len(file_id_list) == 0:
        raise BusinessException(NETDISK_ERR_NO_DEL_FILE)

    # 检查文件是否在同一目录，暂不支持不同目录的文件同时下载(实际原因是不大可能出现此情况，所以懒得写这个代码去支持了^_^!!)。
    src_parent_file = NetdiskSchoolFile.objects.filter(school=user.school, id__in=list(file_id_list), is_del=FALSE_INT).values('parent_id').distinct()
    if src_parent_file.count() > 1:
        raise BusinessException(NETDISK_ERR_FILE_NOTIN_SAMEDIR)

    # 检查我是否有下载权限，只有有下载权限，或者自己的文件可以下载
    cur_user_src_dir_role = api_schooldisk_getuserdirrole(user, src_parent_file.first()['parent_id'])
    if len(set(ROLE_DOWNLOAD) & set(cur_user_src_dir_role)) == 0:
        # 检查是否是我的文件
        if not is_myfile(user.id, file_id_list):
            raise BusinessException(NETDISK_ERR_NOPERMISSION)

    files = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, id__in=list(file_id_list), is_dir=FALSE_INT)
    file_list = list()
    for each_file in files:
        file_dict = dict()
        file_dict['id'] = each_file.id
        url = each_file.fileobj.url if each_file.fileobj else ''

        # 避免数据问题导致程序异常
        if not url:
            continue

        download_url = "/%s/%s?tk=%s" % (settings.FILE_STORAGE_DIR_NAME, url, get_filedownload_token(url)) if url else url
        file_dict['download_url'] = download_url
        file_list.append(file_dict)

    result['file_list'] = file_list
    return result


def get_filedownload_token(file_url):
    # yyyymmddhhmiss,id,salt 再加密
    dt_daytime = today(FORMAT_DATE='%Y%m%d%H%M%S', is_str=True)
    salt = get_rand_str(12)
    file_name = get_filename_from_url(file_url)
    token_str = "%s,%s,%s" % (dt_daytime, file_name, salt)
    token = AES_Obj().encrypt(token_str)
    return token


def get_rand_str(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_filename_from_url(url):
    # 从url中获取文件名及token
    import urlparse
    result = urlparse.urlparse(url)
    file_name = result.path.split('/')[-1]
    return file_name


def get_token_from_url(url):
    # 从url中获取token
    import urlparse
    result = urlparse.urlparse(url)
    param_dict = urlparse.parse_qs(result.query)
    tk = param_dict['tk'][0]
    return tk


def api_oa_send_target(payload):
    response = requests.post(
        urljoin(get_oa_sys_address(), 'api/internal/list/send_target'),
        data=payload,
        timeout=10)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return json.loads(response.text)


def get_oa_sys_address():
    if hasattr(settings, 'OA_INFORMAL_DOMAIN') and settings.OA_INFORMAL_DOMAIN:
        domain = settings.OA_INFORMAL_DOMAIN
    else:
        this_service = Service.objects.filter(code='oa').first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def is_superadmin(user):
    # 检查用户是不是超级管理员(用户中心中配置的该系统的管理员)
    return is_admin_by_user(user)


def api_schooldisk_getuserdirrole(user, dir_file_id):
    result = list()
    # 检查文件夹是不是自己学校的。
    if dir_file_id:
        dir_file = NetdiskSchoolFile.objects.filter(id=dir_file_id, school=user.school, is_del=FALSE_INT).first()
        if not dir_file:
            return result

    # 检查用户是不是超级管理员(用户中心中配置的该系统的管理员)
    if is_superadmin(user):
        result.append(ROLE_TYPE_ADMIN)

    # 如果是根目录，只用在上一步判断是否是超管即可，只有超管有权限，其它人都没有权限。超管只能建目录，不能建文件夹。
    if not dir_file_id:
        return result

    # 获取用户在当前目录的权限,当前目录有的权限我都有。
    result.extend(get_curdir_all_roles(user, dir_file_id))

    # 获取用户在当前目录所有上级目录的权限，上级目录的所有权限自动扩展到下级。
    all_parent_fileid = get_all_parent_fileid(dir_file_id)
    for each_fileid in all_parent_fileid:
        result.extend(get_curdir_all_roles(user, each_fileid))

    # 获取用户下级目录的权限，下级目录有任何权限，自动获取本目录的查看权限。
    all_child_fileid = get_all_child_fileid(user, dir_file_id)
    for each_fileid in all_child_fileid:
        if get_curdir_all_roles(user, each_fileid):
            result.append(ROLE_TYPE_LIST)
            break

    return list(set(result))


def api_schooldisk_getuserfilerole(user, file_id):
    """
    获取用户文件的权限
    用户文件权限即上级文件夹权限，如果文件是自己上传的，则增加一个删除权限和下载权限。
    :param user:
    :param file_id:
    :return:
    """
    cur_file = NetdiskSchoolFile.objects.filter(id=file_id, is_dir=FALSE_INT, is_del=FALSE_INT).first()
    if not cur_file:
        raise BusinessException(NETDISK_ERR_NULL_FILE)

    result = api_schooldisk_getuserdirrole(user, cur_file.parent_id)
    if cur_file.account == user:
        result.extend([ROLE_TYPE_DOWNLOAD, ROLE_TYPE_DEL])
    return list(set(result))


def get_curdir_all_roles(user, dir_file_id):
    result = list()
    # 获取全体用户都有的权限
    role_all_users = NetdiskSchoolRole.objects.filter(account=None, netdiskschoolfile_id=dir_file_id, is_del=FALSE_INT)
    for each_role in role_all_users:
        result.append(each_role.role_type)

    # 获取当前用户在当前目录的权限
    role_cur_user = NetdiskSchoolRole.objects.filter(account=user, netdiskschoolfile_id=dir_file_id, is_del=FALSE_INT)
    for each_role in role_cur_user:
        result.append(each_role.role_type)

    # 用户有任意权限，则自动获取查看权限
    if len(result) > 0:
        result.append(ROLE_TYPE_LIST)
    return list(set(result))


def get_all_parent_fileid(dir_file_id):
    # 获取所有父目录的id
    result = list()
    parent_dir_file_id = dir_file_id
    cycle_count = 1000  # 循环次数控制，避免因为目录结构问题导致死循环。
    while parent_dir_file_id:
        cycle_count = cycle_count - 1
        if cycle_count < 0:
            break

        parent_file = NetdiskSchoolFile.objects.filter(is_del=FALSE_INT, id=parent_dir_file_id).first()
        if parent_file and parent_file.parent_id:
            result.append(parent_file.parent_id)
            parent_dir_file_id = parent_file.parent_id
        else:
            break
    return result


def get_all_child_fileid(user, dir_file_id):
    # 获取所有孩子目录的id
    result = get_childid_flat(user, file_id=dir_file_id, qry_child='1', file_type=None, file_name_like=None, file_name_exact=None)
    return result


def api_schooldisk_dirstatistics(user, dir_file_id):
    # 检查是否是文件夹, 如果为空，则统计整个学校所有的统计情况，如果查询文件夹，则仅查询文件夹下的情况，不包括子文件夹
    if dir_file_id:
        cur_dir = NetdiskSchoolFile.objects.filter(school=user.school, id=dir_file_id, is_dir=TRUE_INT, is_del=FALSE_INT).first()
        if not cur_dir:
            raise BusinessException(NETDISK_ERR_NULL_DIR)

    # 查询需要统计的所有文件
    total_noupload_teacher = ''
    dir_netdisk_file = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, is_dir=FALSE_INT)

    # 非根目录需要统计一个
    if dir_file_id:
        dir_netdisk_file = dir_netdisk_file.filter(parent_id=dir_file_id)
        all_uploadrole_teacherids = get_dir_role_teachers(dir_file_id, ROLE_TYPE_UPLOAD)
        upload_teacher_accountid_list = [each_teacher.account_id for each_teacher in dir_netdisk_file]
        if 'all_teacher' in all_uploadrole_teacherids:
            school_total_teacher_count = Teacher.objects.filter(school=user.school, del_flag=FALSE_INT, is_in=True, is_available=True).count()
            upload_teacher_count = len(set(upload_teacher_accountid_list))
            total_noupload_teacher = school_total_teacher_count - upload_teacher_count
        else:
            upload_role_teacher_accountid_list = [each_teacher['account_id'] for each_teacher in all_uploadrole_teacherids]
            total_noupload_teacher = len(set(upload_role_teacher_accountid_list) - set(upload_teacher_accountid_list))

    dir_netdisk_cnt = dir_netdisk_file.count()
    today_file_cnt = dir_netdisk_file.filter(create_time__gte=today()).count()
    total_upload_people = dir_netdisk_file.values('account_id').distinct().count()

    result = {
        "file_count": dir_netdisk_cnt,
        "today_file_count": today_file_cnt,
        "total_upload_teacher": total_upload_people,
        "total_noupload_teacher": total_noupload_teacher,
    }
    return result


def api_schooldisk_dayuploadinfo(user, startdate, enddate, dir_file_id):
    result = list()
    if not enddate:
        enddate = today(FORMAT_DATE='%Y-%m-%d', is_str=False)
    else:
        enddate = str2datetime(enddate, '%Y-%m-%d')

    if not startdate:
        startdate = enddate + datetime.timedelta(days=-30)
    else:
        startdate = str2datetime(startdate, '%Y-%m-%d')

    day_list = get_day_list(startdate, enddate)

    for each_day in day_list:
        day_cycle = get_day_cycle(each_day)
        upload_day_count = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, is_dir=FALSE_INT,
                                                            create_time__gte=day_cycle['startdate'], create_time__lte=day_cycle['enddate'])
        if dir_file_id:
            upload_day_count = upload_day_count.filter(parent_id=dir_file_id)

        upload_day_count = upload_day_count.count()

        day_dict = {
            'day': datetime2str(day_cycle['startdate'], format='%Y-%m-%d'),
            'count': upload_day_count,
        }
        result.append(day_dict)

    return result


def api_schooldisk_alldirsummary(user):
    result = list()
    all_dir = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, is_dir=TRUE_INT)
    for each_dir in all_dir:
        son_files = NetdiskSchoolFile.objects.filter(school=user.school, is_del=FALSE_INT, is_dir=FALSE_INT, parent_id=each_dir.id)
        totolsize = 0
        for each_son in son_files:
            totolsize = totolsize + each_son.fileobj.size
        dir_dict = {
            "dir_file_id": each_dir.id,
            "dir_name": each_dir.name,
            "dir_size_b": totolsize,
            "dir_size": get_friendly_size(totolsize),
            "dir_updatetime": datetime2str(each_dir.update_time, format="%Y-%m-%d %H:%M:%S"),
        }
        result.append(dir_dict)

    return result
