# -*- coding=utf-8 -*-

import platform

from base import *

DEBUG = True

UC_INFORMAL_DOMAIN = 'http://usercenter-test.hbeducloud.com/school_center_dev/'
LOCAL_INFORMAL_DOMAIN = 'http://127.0.0.1:8000'

CAS_SERVER_URL = "http://10.1.3.61:81/sso/"

LOGIN_URL ='/html/locallogin'

if 'Windows' in platform.platform():
    dbcharset = 'utf8'
else:
    dbcharset = 'utf8mb4'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hx_netdisk',
        'USER': 'admin',
        'PASSWORD': '111111',
        'HOST': '192.168.5.175',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset': dbcharset},
    },
    # school_center real-time DB for query
    'school_center': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_center',
        'USER': 'admin',
        'PASSWORD': '111111',
        'HOST': '192.168.5.175',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
    }
}


OA_INFORMAL_DOMAIN = 'http://oa-test.hbeducloud.com'  # oa接口地址

USE_S3 = False

AWS_ACCESS_KEY_ID = "5NT2CU6KQE2Y34SGZTGT"
AWS_SECRET_ACCESS_KEY = "wfV2aMpXEiskrDnDPOoM1LU5ILgTJxMLdBDWBSIu"
AWS_STORAGE_BUCKET_NAME = "netdisk_test"
AWS_S3_HOST = "127.0.0.1"
AWS_S3_PORT = 58000

USE_MSG = False

USE_USER_CENTER_DB_LOGIN = False
SERVICE_USER_CENTER_BUCKET = "school_center_dev"

DATA_STORAGE_USE_S3 = False   # 断点续传是否采用S3对象存储
