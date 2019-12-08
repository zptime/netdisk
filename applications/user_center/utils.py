# -*- coding=utf-8 -*-
import json
import datetime
import urllib2
import urllib
import re
import logging
import itertools
import functools
import traceback
import random
from urlparse import urlparse
from django import http
from django.conf import settings
from django.utils.decorators import method_decorator
from ipaddr_fun import get_subnet_list, ip_in_subnet_list

logger = logging.getLogger(__name__)

# 标志位
FLAG_YES = 1
FLAG_NO = 0

# error code
ERR_SUCCESS = [0, u'完成']
ERR_REQUESTWAY = [40006, u'请求方式错误']
ERR_MODEL_NAME_ERR = [40025, u"模块名称不存在"]
ERR_LOGIN_FAIL = [40003, u'用户名或密码错误']
ERR_USER_NOTLOGGED = [40004, u'用户未登录']
ERR_USER_AUTH = [40005, u'用户权限不够']
ERR_ITEM_NOT_EXIST = [40007, u'记录不存在']

# 用户类型
USER_TYPE_STUDENT = 1
USER_TYPE_TEACHER = 2
USER_TYPE_PARENT = 4

# 时间格式
DATE_FORMAT_MONTH = 2
DATE_FORMAT_DAY = 3
DATE_FORMAT_TIME = 4
SECONDS_PER_DAY = 24*60*60

# 是否检查登录
IS_CHECK_LOGIN = True


# 科目/章节
ERR_SUBJECT_HAVE_EXIST_ERROR = [40060, u'科目已经存在']
ERR_SUBJECT_ID_ERROR = [40061, u'科目ID不正确']
ERR_SUBJECT_GRADE_NUM_ERROR = [40062, u'科目的年级设置不正确']
ERR_TEXTBOOK_HAVE_EXIST_ERROR = [40063, u'教材已经存在']
ERR_TEXTBOOK_ID_ERROR = [40064, u'教材ID不正确']
ERR_CHAPTER_ID_ERROR = [40065, u'章节ID不正确']

# 职务
INIT_TITLE_LIST = [{"name": u"教师", "comments": u"普通学校人员默认为教师"},
                   {"name": u"班主任", "comments": u"管理班级和班级学生，可在班级管理中添加"},
                   {"name": u"校长", "comments": u"查看全校师生信息，拥有学校管理权"}]
TITLE_NAME_TEACHER = INIT_TITLE_LIST[0]["name"]
TITLE_NAME_CLASSMASTER = INIT_TITLE_LIST[1]["name"]
TITLE_NAME_SCHOOLMASTER = INIT_TITLE_LIST[2]["name"]
INIT_TITLE_NAME_LIST = [TITLE_NAME_TEACHER, TITLE_NAME_CLASSMASTER, TITLE_NAME_SCHOOLMASTER]


def auth_check(request, method="POST", check_login=True):
    dict_resp = {}

    log_request(request)
    if not IS_CHECK_LOGIN:
        return dict_resp

    if check_login:
        if not request.user.is_authenticated():
            dict_resp = {'c': ERR_USER_NOTLOGGED[0], 'e': ERR_USER_NOTLOGGED[1]}
            return dict_resp
    if request.method != method.upper():
        dict_resp = {'c': ERR_REQUESTWAY[0], 'e': ERR_REQUESTWAY[1]}
        return dict_resp

    return dict_resp


def log_request(request):
    # self.start_time = time.time()
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
    if hasattr(request, 'user'):
        user_account = getattr(request.user, 'username', '-')
    else:
        user_account = 'nobody-user'
    if 'POST' == str(request.method):
        logger.info('[POST] %s %s %s :' % (remote_addr, user_account, request.get_full_path()))
        # info(request.POST)
    if 'GET' == str(request.method):
        logger.info('[GET] %s %s %s :' % (remote_addr, user_account, request.get_full_path()))
        # info(request.GET)


def internal_or_403(view_func):
    """
    A view decorator which returns the provided view function,
    modified to return a 403 when the remote address is not in
    the list of internal IPs defined in settings.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            subnet_list = get_subnet_list()
            if not ip_in_subnet_list(request.META['REMOTE_ADDR'], subnet_list):
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')
            return view_func(request, *args, **kwargs)
        except Exception as ex:
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    return wrapper


class Internal(object):
    """
    A mix-in for class based views, which disallows requests from
    non-internal IPs.
    """
    @method_decorator(internal_or_403)
    def dispatch(self, *args, **kwargs):
        return super(Internal, self).dispatch(*args, **kwargs)


# 请求第三方网站数据
def send_http_request(url, method="POST", form_data_dict={}, file_data_dict={}):
    # Create the form with simple fields
    form = MultiPartForm()
    for key, value in form_data_dict.items():
        form.add_field(key, value)
    for key, value in file_data_dict.items():
        form.add_file(key, value[0], value[1])

    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)

    # build a request
    data = str(form)
    request = urllib2.Request(url, data=data)

    # add any other information you want
    request.add_header("Content-Type", form.get_content_type())
    request.add_header('Content-length', len(data))
    # overload the get method function with a small anonymous function...
    request.get_method = lambda: method

    try:
        connection = opener.open(request, timeout=settings.REQUEST_CONNECTION_TIMEOUT_SECONDS)
    except urllib2.HTTPError, e:
        # connection = e
        logger.error("Request ERROR url: %s method: %s form_data_dict: %s" % (url, method, str(form_data_dict)))
        raise Exception(u"无法连接到网站")

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        data = connection.read()
        return data
    else:
        # handle the error case. connection.read() will still contain data
        # if any was returned, but it probably won't be of any use
        logger.error("Request ERROR response_code: %s url: %s method: %s form_data_dict: %s" % (str(connection.code),
                                                                                                url, method,
                                                                                                str(form_data_dict)))
        raise Exception(u"请求网站返回值不是200")


def try_send_http_request(domain_list, path, method="POST", form_data_dict={}, file_data_dict={}):
    random.shuffle(domain_list)
    for domain in domain_list:
        url = domain + path
        try:
            return send_http_request(url, method, form_data_dict, file_data_dict)
        except Exception as ex:
            logger.error("Connect [%s] error, Try another url", url)
            sErrInfo = traceback.format_exc()
            logger.error(sErrInfo)
            continue
    logger.error("Have try all domain of this service but not found an available one")
    raise Exception(u"无法连接到网站")


class RoundTripEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                "_type": "datetime",
                "value": obj.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                ))
            }
        return super(RoundTripEncoder, self).default(obj)


class RoundTripDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'datetime':
            return datetime.datetime.strptime(obj['value'], '%Y-%m-%d %H:%M:%S')
        return obj


def convert_datetime_to_str(date, date_format=DATE_FORMAT_DAY):
    try:
        date_str = date.strftime('%Y-%m-%d')
        if date_format == DATE_FORMAT_MONTH:
            date_str = date.strftime('%Y-%m')
        elif date_format == DATE_FORMAT_TIME:
            date_str = date.strftime('%Y-%m-%d %H:%M:%S')
        return date_str
    except Exception as ex:
        # logger.warn("datetime_to_str fail")
        return ""


def get_domain_name(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def get_main_domain(url):
    if check_ip_url(url):
        return ""
    # 获取域名
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    # 去除子域名
    i = domain.index(".")
    domain = domain[i+1:]
    # 去除端口
    j = domain.find(":")
    if j > 0:
        domain = domain[:j]
    if domain:
        return domain
    else:
        return ""


def check_ip_url(url):
    pattern = "(\\d*\\.){3}\\d*"
    matchObj = re.search(pattern, url)
    if matchObj:
        return True
    else:
        return False


def convert_list_to_dict(src_list, key_name):
    ret_dict = {}
    for item in src_list:
        key = item.pop(key_name)
        if key not in ret_dict.keys():
            ret_dict[key] = []
        ret_dict[key].append(item)
    return ret_dict


import mimetools
import mimetypes


def convert_utf8_to_str(s):
    if isinstance(s, unicode):
        s = s.encode("utf-8")
    return s
        

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        name = convert_utf8_to_str(name)
        value = convert_utf8_to_str(value)
        self.form_fields.append((str(name), str(value)))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        fieldname = convert_utf8_to_str(fieldname)
        filename = convert_utf8_to_str(filename)
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((str(fieldname), str(filename), str(mimetype), body))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )

        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)