# -*- coding=utf-8 -*-

from base import *

DEBUG = True

UC_INFORMAL_DOMAIN = 'http://usercenter-test.hbeducloud.com/school_center_dev/'
# LOCAL_INFORMAL_DOMAIN = 'http://127.0.0.1:8000'

CAS_SERVER_URL = "http://test-sso.hbeducloud.com:8088/sso/"

LOGIN_URL ='/html/login'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hx_netdisk',
        'USER': 'admin',
        'PASSWORD': 'fhcloud86Fh12#$',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset' : 'utf8mb4'},
    },
    # school_center real-time DB for query
    'school_center': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_center',
        'USER': 'root',
        'PASSWORD': '111111',
        'HOST': '192.168.100.42',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
    }
}

USE_S3 = True

AWS_ACCESS_KEY_ID = "5NT2CU6KQE2Y34SGZTGT"
AWS_SECRET_ACCESS_KEY = "wfV2aMpXEiskrDnDPOoM1LU5ILgTJxMLdBDWBSIu"
AWS_STORAGE_BUCKET_NAME = "netdisk_test"
AWS_S3_HOST = "192.168.200.100"
AWS_S3_PORT = 8000

USE_MSG = True

USE_USER_CENTER_DB_LOGIN = True
SERVICE_USER_CENTER_BUCKET = "school_center_dev"
