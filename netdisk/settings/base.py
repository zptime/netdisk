# -*- coding=utf-8 -*-

import os

# 系统错误码前缀:
SYSTEM_CODE = '22'

DB_ADMIN = 'root'

# 本系统包含的对外服务
SYSTEM_NAME = 'netdisk'
SYSTEM_DESC = u'网盘'
SYSTEM_SERVICES = (SYSTEM_NAME,)
SERVICE_SYSTEM_SPLIT_CHAR = '@'

SECRET_KEY = '0f$@gun=@7es+9t%m%u7xl$g&kqar$ptt-xpc99lkdn6j_fmjn'

WSGI_APPLICATION = SYSTEM_NAME + '.wsgi.application'

ROOT_URLCONF = SYSTEM_NAME + '.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

TEMP_DIR = os.path.join(BASE_DIR, 'temp')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

MEDIA_PATH_PUBLIC = 'media/public/'
MEDIA_PATH_PROTECT = 'media/protected/'

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'user_center.Account'

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'applications.swagger',
    'applications.bizlog',
    'applications.common',
    'applications.user_center',
    'applications.netagent',
    'applications.upload_resumable',
    'applications.personaldisk',
    'applications.schooldisk',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'applications.bizlog.utils.Log2DBMiddleware'
)

# 本地认证结合CAS认证
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SUIT_CONFIG = {
    'ADMIN_NAME': u'华校网盘SaaS数据管理',
    'HEADER_DATE_FORMAT': '',
    'HEADER_TIME_FORMAT': 'H:i',
    'LIST_PER_PAGE': 50,
    'MENU': (
        {'app': 'common', 'label': u'通用',},
    )
}

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'django.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'django_command': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'command.log'),
            'formatter': 'standard',
        },
        'django.db.backends_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'db.log'),
            'formatter': 'standard',
        },
        'business_exception': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'biz_except.log'),
            'formatter': 'standard',
        },
        'sync_user_data': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'sync_user_data.log'),
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
        'applications': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django_command': {
            'handlers': ['django_command', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'business_exception': {
            'handlers': ['business_exception', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'applications.user_center': {
            'handlers': ['sync_user_data', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_S3_USE_SSL = False
from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

CAS_VERSION = "3"
CAS_IGNORE_REFERER = True
CAS_CREATE_USER = False

# 用户中心相关参数
REQUEST_CONNECTION_TIMEOUT_SECONDS = 30
SERVICE_USER_CENTER = "user_center"
SERVICE_USER_CENTER_BUCKET = "school_center"
USER_CENTER_S3_HOST = ""
API_USER_CENTER_LIST_SUBNET = "/open/list/subnet"
API_USER_CENTER_DETAIL_UPDATE_TIME = "/open/detail/update_time"
API_USER_CENTER_LIST_ITEMS = "/open/list/items"
API_USER_CENTER_CALL_API = "/open/call/api"
API_USER_CENTER_APP_REFRESH_ITEM = "/user_center/api/refresh/item"

# 同步用户中心哪些数据库表
MODEL_SYNC_FROM_USER_CENTER = \
    ["Subnet", "School", "Grade", "Class", "Account", "Student",
     "Parent", "ParentStudent", "Title", "Teacher", "TeacherClass",
     "Subject", "TeacherSubject", "Service", "SchoolService", "Role",
     "UserRole", "Textbook", "TeacherTextbook", "SchoolTextbook"]

SESSION_COOKIE_AGE = 90 * 24 * 60 * 60

# 自定义HTTP请求消息头，用于移动设备标识客户端用户类型与学校
HTTP_HEADER_CURRENT_USER_TYPE = 'CURRENT_USER_TYPE'


# crop图片长宽
PICTURE_CROP_WIDTH = 300

# 宽大于多少的图片需要压缩
PICTURE_NEED_THUMB_WIDTH = 1000

# 高大于多少的图片需要压缩
PICTURE_NEED_THUMB_HEIGHT = 1000

# 缩略图 and 裁剪图 格式
PICTURE_CROP_FORMAT = PICTURE_THUMB_FORMAT = 'png'


# upload_resumable
# TMP_DIR = os.path.join(BASE_DIR, 'tmp_file')
DATA_STORAGE_USE_S3 = True   # 是否采用S3对象存储
DATA_STORAGE_USE_S3_HOST_URL = False  # 若该参数为真，文件URL使用S3 HOST做为域名
DATA_STORAGE_USE_ABSOLUTE_URL = False  # 默认是否采用绝对地址
FILE_STORAGE_DIR_NAME = "media"
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# 静态文件token生成密码
PASSWORD_CRYPT_KEY = "58560e24317140589770c1af3bb2905c"
# 静态文件超时时间(秒) 当前1天
STATIC_FILE_TIMEOUT = 60*60*24*1
