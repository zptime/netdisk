# -*- coding=utf-8 -*-

import json
import logging
import re, sys
import random
import datetime
import uuid
import math
from binascii import a2b_hex, b2a_hex

from Crypto.Cipher import AES
from pypinyin import lazy_pinyin, FIRST_LETTER, NORMAL

from utils.const_def import *
from utils.const_err import *
from utils.utils_except import BusinessException
# from utils.utils_type import smart_unicode
from utils.utils_type import var2unicode

logger = logging.getLogger(__name__)


def guid_by_uuid():
    """
        通过uuid生成唯一标识符
    """
    return str(uuid.uuid1()).replace('-', '')


def guid_by_time():
    """
        通过当前时间生成唯一标识符(20位)
    """
    fn = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
    fn += '%d' % random.randint(10, 99)
    return fn


def cut_last_char(raw, char_def=';'):
    if raw.endswith(char_def):
        return raw[0:-1]
    else:
        return raw


def random_code(length):
    """
        随机生成验证码
    """
    num = '0123456789'
    return ''.join(random.sample(num, length))


def is_duplicate_field(app_name, model_name, field_name, value, del_str='is_del'):
    models_file_name = app_name + '.models'
    __import__(models_file_name)
    model_clazz = getattr(sys.modules[models_file_name], model_name)
    query_para = {
        del_str: False,
        field_name: value
    }
    return model_clazz.objects.filter(**query_para).exists()


def is_valid_idcard(id):
    """
        身份证合法性验证
    """
    id = id.upper()
    c = 0
    for (d, p) in zip(map(int, id[:~0]), range(17, 0, -1)):
        c += d * (2 ** p) % 11
    return id[~0] == '10X98765432'[c % 11]


def is_chinese_str(raw_string, mode=1):
    """
        判断是否为中文字符串
        mode:
        1: 是不是全部是中文 
        2: 是不是包含中文 
        3: 是不是以中文开头
    """
    string = var2unicode(raw_string.lstrip())
    if mode == 1:
        for x in string:
            if not (x >= u'\u4e00' and x <= u'\u9fa5'):
                return False
        return True
    elif mode == 2:
        for x in string:
            if (x >= u'\u4e00' and x <= u'\u9fa5'):
                return True
        return False
    elif mode == 3:
        if len(string) > 0:
            x = string[0]
            return (x >= u'\u4e00' and x <= u'\u9fa5')
        else:
            return False
    else:
        return False


def random_int_len(start, end, length):
    nums = range(start, end)
    data = random.sample(nums, length)
    return data


def mask_words(words, content):
    """
        替换敏感词
        敏感词用逗号分割
    """
    if not words:
        return content
    try:
        lst = words.split(',')
        for w in lst:
            content = content.replace(w, '**')
    except:
        logger.exception('')
    return content


def remove_html_tag(html):
    """
        去除html标签
    """
    reg = re.compile('<[^>]*>')
    return reg.sub('', html)


def copy_attr_include(src, destiny, include=()):
    for each in include:
        setattr(destiny, each, getattr(src, each))


def print_json(raw_obj):
    """
        将字典/列表等格式漂亮输出成json格式
    """
    print json.dumps(raw_obj, ensure_ascii=False, indent=4)


def filter_with_tuple(model_name_abs, fields_list, tuple_list, del_str='is_del', kickout_del=True):
    """
        组合条件查询
        model_name example: applications.user_center.models.Account
    """
    if not tuple_list:
        return None
    _index = model_name_abs.rfind('.')
    model_name = model_name_abs[_index+1:]
    pkg = model_name_abs[:_index]
    __import__(pkg)
    model_clazz = getattr(sys.modules[pkg], model_name)
    query_para = {
        del_str: False,
    }
    fields_str = ','.join(fields_list)
    _tmp_list = list()

    for each in tuple_list:
        _tmp_list.append('(%s)'% ','.join([str(x) for x in each]))
    values_str = ','.join(_tmp_list)
    _qs_1 = model_clazz.objects.extra(where=['(%s) in (%s)' % (fields_str, values_str)])
    if kickout_del:
        _qs_2 = _qs_1.filter(**query_para)
    return _qs_2


def contains_emoji(content):
    if not content:
        return False
    content_unicode = var2unicode(content)
    for each in content_unicode:
        if u"\U0001F600" <= each and each <= u"\U0001F64F":
            return True
        elif u"\U0001F300" <= each and each <= u"\U0001F5FF":
            return True
        elif u"\U0001F680" <= each and each <= u"\U0001F6FF":
            return True
        elif u"\U0001F1E0" <= each and each <= u"\U0001F1FF":
            return True
        else:
            continue
    return False


def get_terminal_type(useragent):
    """
        通过useragent获取最后使用的设备
    """
    if 'FengHuoVXiao' in useragent:
        return MOBILE_TYPE_APPLE_PHONE
    elif 'okhttp' in useragent:
        return MOBILE_TYPE_ANDROID_PHONE
    return PC_TYPE_DEFAULT


def get_pages(cnt, page, size):
    """
         分页，这种方式比Paginator更高效一些
        :param:总行数， 当前页码  ，每页行数
        :return: 总页数，本次开始行数，本次结束行数
    """
    page = int(page)
    size = int(size)
    num_pages = math.ceil(float(cnt) / size)  # 总页数
    if page > num_pages:
        raise BusinessException(WRONG_PAGE)
    cur_start = (page - 1) * size
    cur_end = page * size
    return num_pages, cur_start, cur_end


def uid():
    return guid_by_time()


def paging_by_lastid(raw_list, rows):
    rows = int(rows)
    total = len(raw_list)
    max_page = total / rows
    if total % rows != 0:
        max_page += 1

    paged_list = raw_list[:rows]

    result = collections.OrderedDict()
    result['max_page'] = int(max_page)
    result['total'] = int(total)
    result['page'] = 0
    result['data_list'] = list()
    return paged_list, result


def paging_by_page(raw_list, rows, page):
    page = int(page)
    rows = int(rows)
    total = len(raw_list)
    max_page = total / rows
    if total % rows != 0:
        max_page += 1

    if total >= (page - 1) * rows:
        start = (page - 1) * rows
        end = start + rows
        paged_list = raw_list[start:end]
    else:
        paged_list = []

    result = collections.OrderedDict()
    result['max_page'] = int(max_page)
    result['total'] = int(total)
    result['page'] = int(page)
    result['data_list'] = list()
    return paged_list, result


def chinese2pinyin(chinese, first=True):
    style = FIRST_LETTER if first else NORMAL
    unicode_char = var2unicode(chinese)
    pinyin_list = lazy_pinyin(unicode_char, style=style)
    return ''.join(pinyin_list)


"""
    h1  1a  1b  1c         h1   h2   h3
    h2  2a  2b  2c   ==>   1a   2a   3a
    h3  3a  3b  3c         1b   2b   3b
                           1c   2c   3c
"""
def rotate_array(a):
    result = []
    col_count = len(a[0])
    for i in xrange(col_count):
        line = []
        for each in a:
            line.append(each[i])
        result.append(line)
    return result


class AES_Obj():
    def __init__(self):
        self.key = 'D8fc69MF2x45GpC7'
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
