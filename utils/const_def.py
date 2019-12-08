# -*- coding: utf-8 -*-

import collections

# --------------------------------- 统一常量定义（一般不应修改） ------------------------------------

# 数据表中URL最大长度
from collections import defaultdict


# '是'与'否'定义
TRUE_STR = '1'
FALSE_STR = '0'
TRUE_INT = 1
FALSE_INT = 0

# 用户类型
USER_TYPE_NONE = 0     # 未定义
USER_TYPE_STUDENT = 1  # 学生
USER_TYPE_TEACHER = 2  # 老师
USER_TYPE_PARENT = 4   # 家长
USER_TYPE_STUDENT_TEACHER = 3   # 学生+老师
USER_TYPE_STUDENT_PARENT = 5    # 学生+家长
USER_TYPE_TEACHER_PARENT = 6    # 老师+家长
USER_TYPE_ALL = 7   # 老师+家长+学生
USER_TYPE_MAP = \
    {USER_TYPE_NONE: u'未知', USER_TYPE_STUDENT: u'学生', USER_TYPE_TEACHER: u'老师', USER_TYPE_PARENT: u'家长',
     USER_TYPE_STUDENT_TEACHER: u'学生和老师', USER_TYPE_STUDENT_PARENT: u'学生和家长', USER_TYPE_TEACHER_PARENT: u'老师和家长',
     USER_TYPE_ALL: u'学生、老师和家长',}

TEACHER_DUTY = (USER_TYPE_TEACHER, USER_TYPE_STUDENT_TEACHER, USER_TYPE_TEACHER_PARENT, USER_TYPE_ALL)
STUDENT_DUTY = (USER_TYPE_STUDENT, USER_TYPE_STUDENT_TEACHER, USER_TYPE_STUDENT_PARENT, USER_TYPE_ALL)
PARENT_DUTY = (USER_TYPE_PARENT, USER_TYPE_STUDENT_PARENT, USER_TYPE_TEACHER_PARENT, USER_TYPE_ALL)

# 设备代号
PC_TYPE_DEFAULT = 0
MOBILE_TYPE_APPLE_PHONE = 1
MOBILE_TYPE_APPLE_PAD = 2
MOBILE_TYPE_ANDROID_PHONE = 4
MOBILE_TYPE_ANDROID_PAD = 8
MOBILE_TYPE_ALL = 15

# 时段类型
DATE_TYPE_STUDYYEAR = 0  # 全部/学年  两个为同一参数，因为最长只能查一个学年的
DATE_TYPE_TODAY = 1  # 当天
DATE_TYPE_THISWEEK = 2  # 本周
DATE_TYPE_THISMONTH = 3  # 本月
DATE_TYPE_LASTMONTH = 4  # 上月
DATE_TYPE_THISSEASON = 5  # 本季度
DATE_TYPE_THISTERM = 6  # 本学期
DATE_TYPE_THISSCHOOLYEAR = 7  # 本学年

DATE_TYPE_DAY = 1  # 当天
DATE_TYPE_WEEK = 2  # 本周
DATE_TYPE_MONTH = 3  # 本月

DEFAULT_FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"

# 翻页模式
PagingMode = collections.namedtuple('PagingMode', ['PAGE', 'SEQ'])
PAGING_MODE = PagingMode(0, 1)

TimeType = collections.namedtuple('TimeType', ['DATE_STD', 'DATE_TRIM', 'DAY_STD', 'DAY_TRIM'])
TIME = TimeType(
    '%Y-%m-%d %H:%M:%S',
    '%y-%m-%d %H:%M:%S',
    '%Y-%m-%d',
    '%y-%m-%d',
)

# 分页默认一页多少条
DEFAULT_PAGE_SIZE = 10

# 系统超级管理员在用户中心的代号
SUPER_ADMIN_CODE = 1

# --------------------------------- 应用常量定义 ------------------------------------

SETTING_DEFAULT_DICT = defaultdict(lambda: '')

# 学校网盘权限类型
# 规则：查看权限自动向上扩散到学校根目录，其它权限自动向下扩散到全部子目录。
# 有管理员/上传/下载权限之一，就自动有查看权限。
# 只有管理员和自己有删除权限。管理员可以删除任意文件、自己只能删除自己的文件。
ROLE_TYPE_NONE = 0  # 无权限
ROLE_TYPE_ADMIN = 1  # 管理员
ROLE_TYPE_LIST = 2  # 查看权限
ROLE_TYPE_UPLOAD = 3  # 上传
ROLE_TYPE_DOWNLOAD = 4  # 下载
ROLE_TYPE_DEL = 5  # 删除

ROLE_ADMIN = (ROLE_TYPE_ADMIN, )  # 管理员权限，可以建立目录，上传下载、删除文件/目录，文件列表
ROLE_LIST = (ROLE_TYPE_ADMIN, ROLE_TYPE_LIST, ROLE_TYPE_UPLOAD, ROLE_TYPE_DOWNLOAD)  # 有任意权限即可列目录
ROLE_UPLOAD = (ROLE_TYPE_ADMIN, ROLE_TYPE_UPLOAD)  # 只有管理员和上传权限可以上传文件
ROLE_DOWNLOAD = (ROLE_TYPE_ADMIN, ROLE_TYPE_DOWNLOAD)  # 只有管理员和下载权限可以下载文件
