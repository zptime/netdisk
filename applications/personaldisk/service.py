# -*- coding=utf-8 -*-
import json
import datetime

from django.db import transaction
from django.db.models import Sum

from applications.common.services import setting_detail
from applications.personaldisk.models import NetdiskPersonalSize, NetdiskPersonalFile
from applications.upload_resumable.models import FileObj
from utils.const_def import *
from utils.const_err import *
from utils.utils_except import BusinessException
from utils.utils_time import today
from utils.utils_tools import get_pages, AES_Obj
import logging
logger = logging.getLogger(__name__)


def api_test(user, type):
    result = get_friendly_size(int(type))
    return result


def api_persondisk_summary(user):
    person_total_size_b = setting_detail("PERSON_MAX_SIZE", user.school)["value"]
    person_size = NetdiskPersonalSize.objects.filter(account_id=user.id, is_del=FALSE_INT).first()

    if person_size:
        person_used_size_b = str(person_size.totalsize)
    else:
        person_used_size_b = "0"

    person_total_size = get_friendly_size(person_total_size_b)
    person_used_size = get_friendly_size(person_used_size_b)

    result = {
        "person_total_size_b": person_total_size_b,
        "person_used_size_b": person_used_size_b,
        "person_total_size": person_total_size,
        "person_used_size": person_used_size,
    }
    return result


def get_friendly_size(size):
    # 把字节转换成BKMGT的形式。
    size = int(size)
    size_dict = {
        "B": 1024 ** 0,
        "K": 1024 ** 1,
        "M": 1024 ** 2,
        "G": 1024 ** 3,
        "T": 1024 ** 4,
    }
    unit = "B"  # 默认单位为B
    for each_size_dict in ("B", "K", "M", "G", "T"):
        if size >= size_dict[each_size_dict]:
            unit = each_size_dict
        else:
            break

    # 如果单位是B则不带小数，其它情况全部带2位小数
    if unit == "B":
        result = "%d%s" % (float(size)/size_dict[unit], unit)
    else:
        result = "%.2f%s" % (float(size)/size_dict[unit], unit)

    return result


def api_persondisk_adddir(user, dir_name, file_id):
    # 文件名不能为空
    if not dir_name:
        raise BusinessException(NETDISK_ERR_FILENAME)

    # 检查上级文件夹是否存在, 检查是否存在同名的文件夹。
    if file_id:
        cur_dir = NetdiskPersonalFile.objects.filter(id=file_id, account_id=user.id, is_del=FALSE_INT).first()
        if not cur_dir:
            raise BusinessException(NETDISK_ERR_NULL_DIR)
        file_same_names = NetdiskPersonalFile.objects.filter(account_id=user.id, is_del=FALSE_INT, name=dir_name, is_dir=TRUE_INT, parent_id=file_id)
    else:
        file_same_names = NetdiskPersonalFile.objects.filter(account_id=user.id, is_del=FALSE_INT, name=dir_name, is_dir=TRUE_INT, parent_id=None)

    if file_same_names:
        raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

    # 增加文件夹
    netdiskpersonalfile = NetdiskPersonalFile()
    netdiskpersonalfile.account = user
    netdiskpersonalfile.name = dir_name
    netdiskpersonalfile.is_dir = TRUE_INT
    netdiskpersonalfile.fileobj = None
    netdiskpersonalfile.parent_id = file_id if file_id else None
    netdiskpersonalfile.save()

    result = {
        "file_id": netdiskpersonalfile.id,
    }
    return result


def api_persondisk_modname(user, file_name, file_id):
    # 文件名不能为空,目前只能修改目录。
    if not file_name:
        raise BusinessException(NETDISK_ERR_FILENAME)
    if not file_id:
        raise BusinessException(REQUEST_PARAM_ERROR)

    if not is_myfile(user.id, [file_id]):
        raise BusinessException(NETDISK_ERR_NOPERMISSION)

    # 检查文件是否存在，检查是否有新的同名文件夹
    cur_file = NetdiskPersonalFile.objects.filter(id=file_id, account_id=user.id, is_del=FALSE_INT).first()
    if not cur_file:
        raise BusinessException(NETDISK_ERR_NULL_DIR)
    file_same_names = NetdiskPersonalFile.objects.filter(account_id=user.id, is_del=FALSE_INT, name=file_name, is_dir=TRUE_INT,
                                                         parent_id=cur_file.parent_id).exclude(id=file_id)
    if file_same_names:
        raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

    cur_file.name = file_name
    cur_file.save()

    result = {
        "file_id": cur_file.id,
        "file_name": cur_file.name,
    }
    return result


def is_myfile(account_id, file_id_list):
    # 检查是不是我的网盘文件
    file_id_list = list(set(file_id_list))  # 去重
    netdiskfilecnt = NetdiskPersonalFile.objects.filter(account_id=account_id, id__in=file_id_list, is_del=FALSE_INT).count()
    return True if netdiskfilecnt >= len(file_id_list) else False


@transaction.atomic
def api_persondisk_submitfile(user, file_id, file_obj_id_list):
    if not file_obj_id_list:
        raise BusinessException(REQUEST_PARAM_ERROR)

    # 限制只允许老师使用
    if user.type != USER_TYPE_TEACHER:
        raise BusinessException(AUTH_WRONG_TYPE)

    if file_id:
        # 检查目标文件夹是否存在
        cur_file = NetdiskPersonalFile.objects.filter(id=file_id, is_dir=TRUE_INT, account_id=user.id, is_del=FALSE_INT).first()
        if not cur_file:
            raise BusinessException(NETDISK_ERR_NULL_DIR)

    file_obj_id_list = json.loads(file_obj_id_list)

    totalspace = 0
    for each_fileid in file_obj_id_list:
        # 检查文件是否存在，并且是自己上传
        fileobj = FileObj.objects.filter(id=each_fileid, del_flag=FALSE_INT).first()
        if not fileobj:
            raise BusinessException(NETDISK_ERR_NO_FILEOBJ)

        parent_id = file_id if file_id else None

        # 检查是否有同名的文件
        file_same_names = NetdiskPersonalFile.objects.filter(account_id=user.id, is_del=FALSE_INT, name=fileobj.name, is_dir=FALSE_INT,
                                                             parent_id=parent_id)
        if file_id:
            file_same_names = file_same_names.filter(parent_id=file_id)

        if file_same_names:
            raise BusinessException(NETDISK_ERR_HAS_SAMEFILE)

        netdiskpersonalfile = NetdiskPersonalFile()
        netdiskpersonalfile.account = user
        netdiskpersonalfile.name = fileobj.name
        netdiskpersonalfile.is_dir = FALSE_INT
        netdiskpersonalfile.fileobj = fileobj
        netdiskpersonalfile.parent_id = parent_id
        netdiskpersonalfile.save()

        totalspace = totalspace + fileobj.size

    # 刷新使用空间。
    # person_total_size_b = api_persondisk_summary(user)['person_total_size_b']
    # person_used_size_b = api_persondisk_summary(user)['person_used_size_b']
    #
    # if totalspace > person_total_size_b - person_used_size_b:
    #     raise BusinessException(NETDISK_ERR_SPACE_NOENOUPH)
    if not refresh_user_space(user):
        raise BusinessException(NETDISK_ERR_SPACE_NOENOUPH)
    return 'ok'


def api_persondisk_filelist(user, file_id, qry_child, file_type, file_name_like, file_name_exact, size, page, last_id):
    # 查询文件列表
    result = dict()
    parent_id = file_id if file_id else None
    if parent_id:
        parent_file = NetdiskPersonalFile.objects.filter(id=parent_id, is_del=FALSE_INT).first()
        result['id'] = parent_file.id
        result['pid'] = parent_file.parent_id if parent_file.parent_id else 1
        result['filename'] = parent_file.name
        result['sizeb'] = parent_file.fileobj.size if parent_file.fileobj else ''
        result['size'] = get_friendly_size(result['sizeb']) if result['sizeb'] else ''
        result['is_dir'] = parent_file.is_dir
        result['update_time'] = parent_file.update_time.strftime(DEFAULT_FORMAT_DATETIME)
    else:
        result['id'] = 1  # 不要问我为什么，前端要求根目录id为1，pid为0
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

    netdiskfiles = NetdiskPersonalFile.objects.filter(account=user, parent_id=parent_id, is_del=FALSE_INT)
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
        child = dict()
        child['id'] = each_file.id
        child['pid'] = each_file.parent_id if each_file.parent_id else 1  # 父节点ID，前端要的
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

    netdiskfiles = NetdiskPersonalFile.objects.filter(account=user, parent_id=parent_id, is_del=FALSE_INT)
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
def api_persondisk_delfile(user, file_id_list, file_id_del_all):
    if file_id_list:
        file_id_list = json.loads(file_id_list)
    elif file_id_del_all:
        file_id_list = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, parent_id=file_id_del_all).values_list('id', flat=True)
    else:
        file_id_list = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, parent_id=None).values_list('id', flat=True)

    if len(file_id_list) == 0:
        raise BusinessException(NETDISK_ERR_NO_DEL_FILE)

    # 检查是否是我的文件
    if not is_myfile(user.id, file_id_list):
        raise BusinessException(NETDISK_ERR_NOPERMISSION)

    del_fileid_list = list()
    for each_file_id in file_id_list:
        del_fileid_list.append(each_file_id)
        del_fileid_list.extend(get_childid_flat(user, file_id=each_file_id, qry_child=1, file_type=None, file_name_like=None, file_name_exact=None))

    NetdiskPersonalFile.objects.filter(id__in=list(del_fileid_list)).update(is_del=TRUE_INT)

    refresh_user_space(user)

    return 'ok'


@transaction.atomic
def api_persondisk_movfile(user, src_file_id_list, desc_file_id, file_id_move_all):
    if src_file_id_list:
        src_file_id_list = json.loads(src_file_id_list)
    elif file_id_move_all:
        src_file_id_list = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, parent_id=file_id_move_all).values_list('id', flat=True)
    else:
        src_file_id_list = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, parent_id=None).values_list('id', flat=True)

    # 检查来源文件是否是我的文件
    if not is_myfile(user.id, src_file_id_list):
        raise BusinessException(NETDISK_ERR_NOPERMISSION)
    # 检查目标文件是否是我的文件
    if desc_file_id and not is_myfile(user.id, [desc_file_id]):
        raise BusinessException(NETDISK_ERR_NOPERMISSION)

    # 没传目标文件夹就放到根目录去。
    if not desc_file_id:
        desc_file_id = None

    NetdiskPersonalFile.objects.filter(id__in=list(src_file_id_list), is_del=FALSE_INT).update(parent_id=desc_file_id)

    return 'ok'


def refresh_user_space(user):
    # usedspace = NetdiskPersonalFile.objects.filter(account=user, is_del=FALSE_INT, is_dir=FALSE_INT).values('fileobj.size') \
    #     .aggregate(totalspace=Sum('fileobj.size'))['totalspace']

    usedspace = FileObj.objects.filter(personfileobj__account=user, personfileobj__is_del=FALSE_INT, personfileobj__is_dir=FALSE_INT) \
        .aggregate(totalspace=Sum('size'))['totalspace']
    if not usedspace:
        usedspace = 0

    # 获取总空间
    totalspace = setting_detail('PERSON_MAX_SIZE', user.school)

    if usedspace > totalspace:
        return False
    netdiskpsize, created = NetdiskPersonalSize.objects.update_or_create(account=user,
                                                                         defaults={'is_del': FALSE_INT, 'totalsize': usedspace})
    return True


def api_persondisk_getdownloadurl(user, file_id_list, file_id_get_all):
    result = dict()
    if file_id_list:
        file_id_list = json.loads(file_id_list)
    elif file_id_get_all:
        file_id_list = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, parent_id=file_id_get_all).values_list('id', flat=True)
    else:
        file_id_list = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, parent_id=None).values_list('id', flat=True)

    if len(file_id_list) == 0:
        raise BusinessException(NETDISK_ERR_NO_DEL_FILE)

    # 检查来源文件是否是我的文件
    if not is_myfile(user.id, file_id_list):
        raise BusinessException(NETDISK_ERR_NOPERMISSION)

    files = NetdiskPersonalFile.objects.filter(is_del=FALSE_INT, id__in=list(file_id_list), is_dir=FALSE_INT)
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


def xor_crypt_string(data, key=settings.PASSWORD_CRYPT_KEY, encode=False, decode=False):
    from itertools import izip, cycle
    import base64
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored


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


def api_persondisk_checkauth(user, file_name_in, tk):
    token_str = AES_Obj().decrypt(tk)
    logger.info(token_str)
    token_list = token_str.split(',')
    dt_daytime = token_list[0]
    file_name = token_list[1]
    salt = token_list[2]
    dt_daytime = datetime.datetime.strptime(dt_daytime, '%Y%m%d%H%M%S')
    if datetime.datetime.now() > dt_daytime + datetime.timedelta(seconds=settings.STATIC_FILE_TIMEOUT):
        raise Exception(u'下载文件超时，请重新到网盘下载')

    if file_name_in != file_name:
        raise Exception(u'文件名不一致')
    return 'OK'
