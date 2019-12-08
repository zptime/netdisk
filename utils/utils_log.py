# -*- coding: utf-8 -*-

import json
import logging
import datetime
from functools import wraps

from utils.const_def import *
from utils.const_err import *
from utils.utils_except import BusinessException

logger = logging.getLogger(__name__)
logger_biz_except = logging.getLogger('business_exception')


def log_request(request):
    if settings.DEBUG:
        if hasattr(request, 'user'):
            user_account = getattr(request.user, 'username', '-')
        else:
            user_account = 'anonymous'
        logger.debug('%s %s' % (user_account, request.get_full_path()))


def log_response(request, data):
    if settings.DEBUG:
        logger.debug('request: %s, response json: %s' % (request.get_full_path(), json.dumps(data, ensure_ascii=False)))


def log_exception(e):
    if isinstance(e, BusinessException):
        # 应用捕获异常无需记录Error日志，也无需打印异常堆栈
        logger_biz_except.exception(e)
        logger.warn(e.msg)
    else:
        logger.exception(e)




