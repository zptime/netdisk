# -*- coding: utf-8 -*-

import os
import platform
import socket
import json
import logging
import uuid
from urlparse import urlparse, urljoin

from django.http import HttpResponse
from django.utils import http

from utils.const_def import *
from utils.const_err import *


logger = logging.getLogger(__name__)


def get_host_ip():
    """
        获取当前IP地址
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def response200(result):
    """
        OK
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def response400(result):
    """
        bad request
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=400)


def response403(result):
    """
        Fobbidden
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=403)


def response405(result):
    """
        Method not allowed
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=405)


def response_exception(exception, msg=''):
    from utils.utils_except import BusinessException
    if isinstance(exception, BusinessException):
        final_message = exception.msg
        if msg:
            final_message = u'%s, 原因: %s' % (msg, exception.msg)
        result = {'c': exception.code, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    else:
        final_message = u'请求失败'
        if msg:
            final_message = msg
        result = {'c': -1, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def response_parameter_error(exception):
    dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": exception.message}
    return response400(dict_resp)


def url_with_scheme_and_location(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def url_with_location(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def gen_url_with_fname(url, original_fname):
    """
        生成带有?fname=xxx格式的URL，使得nginx可以增加指定文件名的响应头
    """
    if not url or not original_fname:
        return ''
    (shortname, extension) = os.path.splitext(original_fname)
    return '%s?fname=%s' % (url, shortname)


def get_mac():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def get_mac_last4():
    return ''.join(get_mac().split(':'))[-4:]


g_domain = ''


def url_with_domain(path):
    """
        返回组装了本系统domain的URL
    """
    global g_domain
    if not path:
        return ''
    domain = getattr(settings, 'LOCAL_INFORMAL_DOMAIN', '')
    if not domain:
        if not g_domain:
            from applications.user_center.models import Service
            this_service = Service.objects.filter(code__in=settings.SYSTEM_SERVICES).first()
            if this_service:
                g_domain = url_with_scheme_and_location(this_service.internet_url)
        domain = g_domain
    return urljoin(domain, path)


g_uc_domain = ''


def url_with_uc_domain(fname):
    """
        返回组装了学校管理中心domain的URL
    """
    global g_uc_domain
    if not fname:
        return ''
    uc_domain = getattr(settings, 'UC_INFORMAL_DOMAIN', '')
    if uc_domain:
        return urljoin(uc_domain, fname)
    if not uc_domain:
        if not g_uc_domain:
            from applications.user_center import agents
            url = agents.get_user_center_url()
            g_uc_domain = url
        return g_uc_domain + '/' + settings.SERVICE_USER_CENTER_BUCKET + '/' + fname


