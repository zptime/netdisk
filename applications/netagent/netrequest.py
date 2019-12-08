# coding=utf-8
import json
import logging
from urlparse import urljoin, urlparse

import requests
from django.conf import settings

from applications.user_center.models import Service
from utils.const_err import FAIL
from utils.net_helper import response200

logger = logging.getLogger(__name__)
NETAGENT_SYSTEM_NAME = 'netagent'


def uploadlog(report_path, totaluser, totalrequest, totalrequestunsafe, requestnon200, request500, request200witherror, requestlong, reportlogerror, desription1, desription2, cycle_time):
    """
        上报日志
    """
    payload = {
        'pkg_name': 'applications.mail.services',
        'function_name': 'api_upload_log',
        'parameter': json.dumps({
            'system_code': settings.SYSTEM_NAME,
            'system_name': settings.SYSTEM_DESC,
            'total_user': totaluser,
            'total_request': totalrequest,
            'total_request_unsafe': totalrequestunsafe,
            'request_non_200': requestnon200,
            'request_500': request500,
            'request_200_with_error': request200witherror,
            'request_long': requestlong,
            'report_log_error': reportlogerror,
            'desription1': desription1,
            'desription2': desription2,
            'cycle_time': cycle_time,
            # 'logfile': report_path,  # report_path
        }, ensure_ascii=False)
    }

    files = {'file_in': open(report_path, 'rb')}

    try:
        logger.info('upload log to netagent:')
        logger.info(str(payload).decode("unicode-escape"))
        remote_response = _mail_remote_call(payload, files)
    except Exception as e:
        logger.exception(e)
        return response200({'c': FAIL[0], 'm': FAIL[1], 'd': u'上报日志内容到网络代理平台失败'})
    logger.info('netagent return response:')
    logger.info(str(remote_response).decode("unicode-escape"))
    return remote_response


def sendsms(mobile):
    """
        发送短信
    """
    payload = {
        'pkg_name': 'applications.mail.services',
        'function_name': 'send_message',
        'parameter': json.dumps({
            'mobile': mobile,
        }, ensure_ascii=False)
    }

    try:
        logger.info('sendsms to netagent:')
        logger.info(payload)
        remote_response = _mail_remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return response200({'c': FAIL[0], 'm': FAIL[1], 'd': u'调用网络代理平台失败'})
    logger.info('netagent return response:')
    logger.info(remote_response)
    return remote_response


def sendemail(file_path, mail_sendto, mail_title, mail_content):
    """
    发送电子邮件
    :param file_path: 附件文件路径，为None则不发附件
    :param mail_sendto: 收件人，以逗号隔开
    :param mail_title: 邮件主题
    :param mail_content: 邮件正文
    :return:
    """
    if file_path:
        func_name = 'api_send_mail'
    else:
        func_name = 'api_send_mail_noattach'
    payload = {
        'pkg_name': 'applications.mail.services',
        'function_name': func_name,
        'parameter': json.dumps({
            'mail_sendto': mail_sendto,
            'mail_title': mail_title,
            'mail_content': mail_content,
        }, ensure_ascii=False)
    }

    if file_path:
        files = {'file_in': open(file_path, 'rb')}

    try:
        logger.info('sendmail to netagent:')
        logger.info(str(payload).decode("unicode-escape"))
        if file_path:
            remote_response = _mail_remote_call(payload, files)
        else:
            remote_response = _mail_remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return response200({'c': FAIL[0], 'm': FAIL[1], 'd': u'调用网络代理平台失败'})
    logger.info('netagent return response:')
    logger.info(str(remote_response).decode("unicode-escape"))
    return remote_response


def get_url(url, method, content, timeout):
    """
    通过netagent平台做代理，通过POST或GET方法请求某个URL
    :param url: URL地址
    :param method: 请求方式GET/POST
    :param content: JSON参数字符串
    :param timeout: 超时时间，字符串或数字，不传默认60秒
    :return:
    """
    payload = {
        'pkg_name': 'applications.mail.services',
        'function_name': 'api_get_url',
        'parameter': json.dumps({
            'url': url,
            'method': method,
            'content': content,
            'timeout': timeout,
        }, ensure_ascii=False)
    }

    try:
        logger.info('get url to netagent:')
        logger.info(str(payload).decode("unicode-escape"))
        remote_response = _mail_remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return response200({'c': FAIL[0], 'm': FAIL[1], 'd': u'调用网络代理平台失败'})
    logger.info('netagent return response:')
    logger.info(str(remote_response).decode("unicode-escape"))
    return remote_response


def _mail_remote_call(payload, files=None):
    if files:
        response = requests.post(
            urljoin(get_netagent_log_address(), '/api/internal/proxy'),
            data=payload,
            files=files,
            timeout=60)
    else:
        response = requests.post(
            urljoin(get_netagent_sys_address(), '/api/internal/proxy'),
            data=payload,
            timeout=10)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return json.loads(response.text)


def get_netagent_sys_address():
    if hasattr(settings, 'NETAGENT_INFORMAL_DOMAIN') and settings.NETAGENT_INFORMAL_DOMAIN:
        domain = settings.NETAGENT_INFORMAL_DOMAIN
    else:
        this_service = Service.objects.filter(code__in=[NETAGENT_SYSTEM_NAME, ]).first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def get_netagent_log_address():
    if hasattr(settings, 'NETAGENT_LOG_DOMAIN') and settings.NETAGENT_LOG_DOMAIN:
        domain = settings.NETAGENT_LOG_DOMAIN
    else:
        this_service = Service.objects.filter(code__in=[NETAGENT_SYSTEM_NAME, ]).first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain
