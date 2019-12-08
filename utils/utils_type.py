# -*- coding=utf-8 -*-

import types
import logging
import re
from decimal import Decimal
from utils.const_def import *


logger = logging.getLogger(__name__)


def is_str(data):
    return isinstance(data, basestring)


def is_money(data):
    pattern = r'^(([1-9]{1}\d*)|([0]{1}))(\.(\d){1,2})?$'
    return False if not re.match(pattern, str(data)) else True


def not_null_str(data, default=''):
    """
        将None和数值型转化为String
    """
    if isinstance(data, types.NoneType):
        return default
    elif isinstance(data, types.IntType) or isinstance(data, types.LongType) or isinstance(data, types.FloatType):
        return str(data)
    elif isinstance(data, types.BooleanType):
        return bool2str(data)
    else:
        return data


def div_percent(x, y):
    return '%.2f' % (float(x) / float(y))


def bool2str(bool_para):
    """
        布尔值转字符串
    """
    return '1' if bool_para else '0'


def str2bool(str_para):
    """
        字符串转布尔值
    """
    return False if str_para == '0' else True


def var2unicode(raw):
    """
        任意文本转化为unicode
    """
    if not isinstance(raw, unicode) and not isinstance(raw, str):
        return str(raw).decode('utf8')
    elif isinstance(raw, str):
        return raw.decode('utf8')
    elif isinstance(raw, unicode):
        return raw
    else:
        return None


def unicode2utf8(raw):
    if not isinstance(raw, unicode):
        return str(raw)
    else:
        return raw.encode('utf8')


def float2str(data, decimal):
    """
        将传入的浮点数字，转换为指定小数位的浮点字符串，由于round函数有时会显示有问题
        :type data: 浮点数字(字符串或float类型)
        :type decimal: 小数位数
    """
    formatstr = "%%.%df" % decimal
    return formatstr % data


def str2money(raw):
    """
        将字符串转换为“元.角分”的货币格式，不满足要求则原封不动返回 
    """
    try:
        f = float(raw)
        return '%.2f' % f
    except:
        return raw


def str2money(value, places=2, curr='', sep=',', dp='.', pos='', neg='-', trailneg=''):

    # 当输入为空或不是数值时，返回''
    if not value:
        return ''
    value = value.strip('').replace(',', '')
    try:
        value = Decimal(value)
    except:
        logger.warn('value is not money: %s' % value)
        return ''

    q = Decimal(10) ** -places  # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))

