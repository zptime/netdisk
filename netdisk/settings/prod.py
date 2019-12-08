# -*- coding=utf-8 -*-

from base import *

DEBUG = False

CAS_SERVER_URL = "http://sso.hbeducloud.com/sso/"

LOGIN_URL ='/html/login'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hx_netdisk',
        'USER': 'admin',
        'PASSWORD': 'fhcloud86Fh12#$',
        'HOST': '192.168.100.3',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset' : 'utf8mb4'},
    },
    # school_center real-time DB for query
    'school_center': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_center',
        'USER': 'admin',
        'PASSWORD': 'Fh12#$',
        'HOST': '192.168.100.11',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
    }
}

USE_S3 = True

AWS_ACCESS_KEY_ID = "9X99OHMSGA4ZJO0XZWIO"
AWS_SECRET_ACCESS_KEY = "tm92ArANm1fFeYFC9lXWqgVtTuMPoMfPjRKLljkf"
AWS_STORAGE_BUCKET_NAME = "netdisk_prod"
AWS_S3_HOST = "192.168.200.100"
AWS_S3_PORT = 8000

USE_MSG = True

USE_USER_CENTER_DB_LOGIN = True
