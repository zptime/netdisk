# -*- coding=utf-8 -*-

from django.conf import settings


def code(err_code):
    """
        转换为全局唯一错误码
    """
    return int(settings.SYSTEM_CODE) * 10000 + err_code


# -------------------------------- 通用错误码 （一般不要修改）---------------------------------------

# 以下错误码由用户中心定义
# ERR_REQUESTWAY = [40006, u'请求方式错误']
# ERR_MODEL_NAME_ERR = [40025, u"模块名称不存在"]
# ERR_LOGIN_FAIL = [40003, u'用户名或密码错误']
# ERR_USER_NOTLOGGED = [40004, u'用户未登录']
# ERR_USER_AUTH = [40005, u'用户权限不够']
# ERR_ITEM_NOT_EXIST = [40007, u'记录不存在']

FAIL = [-1, u'失败']
SUCCESS = [0, u'完成']
RATE_LIMIT = [10, u'操作太频繁，请稍后再试']

AUTH_NEED_LOGIN = [40004, u'用户未登录或登录已过期']  # 同用户中心保持一致
AUTH_USER_TYPE_CRUSH = [40000, u'用户角色冲突，请重新登录']

REQUEST_WRONG_METHOD = [code(1000), u'请求方法错误']
REQUEST_INTERNAL = [code(1001), u'无法访问内部接口']
REQUEST_PARAM_ERROR = [code(1002), u'请求参数错误']
AUTH_WRONG_TYPE = [code(1003), u'无权限使用该功能']
AUTH_CONDITION_FAIL = [code(1004), u'由于系统限制, 无法使用该功能']
AUTH_SAME_SCHOOL = [code(1005), u'只能查看本校的相关信息']
AUTH_WRONG_SCHOOL = [code(1006), u'所在学校没有开通该功能']
WRONG_PAGE = [code(1007), u'错误的页码']
WRONG_TIME_TYPE = [code(1008), u'错误的时间类型']
ROOT_FORBID = [code(1009), u'系统管理员不能访问该系统']
USERTYPE_NOT_EXIST = [code(1010), u'用户角色错误']
AUTH_TEACHER_LIST_CLASS_STU = [code(1011), u'不允许查看非任教班级的学生列表']
DATETYPE_ERR = [code(1012), u'错误的时段类型']
PARAM_ERROR_LARGE_STARTDATE = [code(1013), u'起始时间大于结束时间']
TIME_EARLY_THAN_NOW = [code(1014), u'不能早于当前时间']

USER_NOT_EXIST = [code(1100), u'用户不存在']
SCHOOl_NOT_EXIST = [code(1101), u'学校不存在']
CLASS_NOT_EXIST = [code(1102), u'班级不存在']
TEACHER_NOT_EXIST = [code(1103), u'教师不存在']
PARENT_NOT_EXIST = [code(1104), u'家长不存在']
STUDENT_NOT_EXIST = [code(1105), u'学生不存在']
CLIENT_NOT_EXIST = [code(1106), u'终端类型不存在']
IMAGE_NOT_EXIST = [code(1107), u'图片不存在']
TITLE_NOT_EXIST = [code(1108), u'教师头衔不存在']
GRADE_NOT_EXIST = [code(1109), u'年级不存在']


# -------------------------------- 应用定义的错误码 ---------------------------------------

JSON_WRONG = [code(2001), u'请求json格式错误']
SETTING_KEY_WRONG = [code(2002), u'不支持该系统配置参数']

# 文件管理
NETDISK_ERR_FILENAME = [code(2003), u'非法的文件名！']
NETDISK_ERR_NULL_DIR = [code(2004), u'文件夹不存在！']
NETDISK_ERR_HAS_SAMEFILE = [code(2005), u'存在同名文件！']
NETDISK_ERR_NOPERMISSION = [code(2006), u'您无权操作该文件夹/文件！']
NETDISK_ERR_NO_FILEOBJ = [code(2007), u'没有找到对应的文件！']
NETDISK_ERR_SPACE_NOENOUPH = [code(2008), u'空间不足！']
NETDISK_ERR_NO_DEL_FILE = [code(2009), u'无可删除文件！']
NETDISK_ERR_NO_ROLE_MKDIR = [code(2010), u'无权创建文件夹！']
NETDISK_ERR_FILE_NOTIN_SAMEDIR = [code(2011), u'文件不在同一个文件夹！']
NETDISK_ERR_ROOT_NOFILE = [code(2012), u'根目录只允许存放文件夹！']
NETDISK_ERR_NO_PERSONFILE = [code(2013), u'个人网盘中没有找到该文件！']
NETDISK_ERR_NOT_SUPPORT_ROOTQRY = [code(2014), u'不支持查询根目录！']
NETDISK_ERR_NULL_FILE = [code(2015), u'文件不存在！']
