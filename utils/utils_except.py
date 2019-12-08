# -*- coding=utf-8 -*-

import logging


logger = logging.getLogger(__name__)


class BusinessException(Exception):
    """
        业务Exception，通常在view层捕捉
        传入errcode文件中定义的错误信息
        vars is a tuple
    """
    def __init__(self, value, vars=None):
        self.code = value[0]
        self.msg = value[1] if not vars else value[1] % vars

    def __str__(self):
        return repr(self.msg)