# -*- coding: utf-8 -*-

import json
import logging
import datetime

from applications.bizlog.models import OperateLog


logger = logging.getLogger(__name__)


# 以下请求无需记录日志到数据库
EXCLUDE = ('/api/', '/api/docs/', '/api/mobile/heartbeat')


def _save(request, start_time, end_time, response=None, exception=None):
    # 排除不需要记录日志的请求
    if not _is_need_log(request):
        return

    oper_log = OperateLog()
    # 记录请求
    try:
        if request.method == 'GET':
            oper_log.request = (str(request.GET.items())).replace("u\'", "\'").decode('unicode-escape').encode('utf8')
        elif request.method == 'POST':
            request_str = ''
            if request.FILES:
                request_str += u'该请求包含文件上传. '
            if request.POST.items():
                request_str += (str(request.POST.items())).replace("u\'", "\'").decode('unicode-escape').encode('utf8')
            oper_log.request = request_str
        else:
            oper_log.request = u'不支持请求方法为%s的日志记录' % request.method
    except Exception as e:
        logger.exception('oper_log.request encode error')

    # 记录UA
    oper_log.ua = request.META.get('HTTP_USER_AGENT', None)

    # 如果是登录用户，记录用户信息
    if request.user.is_authenticated():
        oper_log.account_id = str(request.user.id)
        oper_log.user_school_id = str(request.user.school.id)
        oper_log.user_type = request.user.type

    # 记录请求头
    oper_log.head = str(request.META)[:500]

    # 记录请求来源IP
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        oper_log.ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        oper_log.ip = request.META['REMOTE_ADDR']

    # 记录请求方法
    oper_log.method = request.method

    # 记录请求开始时间
    oper_log.request_time = start_time

    # 记录请求结束时间
    oper_log.response_time = end_time

    # 记录请求耗时
    oper_log.duration = (end_time - start_time).total_seconds() * 1000 \
            if end_time and start_time and end_time > start_time else 0

    # 记录请求URL
    oper_log.url = request.get_full_path()

    # 当请求抛异常时，记录响应、状态码、C、M
    if exception:
        except_msg = ''
        if hasattr(exception, 'msg'):
            except_msg = exception.msg
        if hasattr(exception, 'message'):
            except_msg = exception.message
        oper_log.response = except_msg
        oper_log.status_code = '500'
        oper_log.c = -1
        oper_log.m = u'服务器内部异常: %s' % except_msg

    # 当有处理结果时，记录响应、状态码、C、M
    elif response:
        try:
            if response['Content-Type'] != 'application/json':
                oper_log.response = response['Content-Type']
            else:
                oper_log.response = (str(response)).decode('utf8')[:20000].encode('utf8')
        except Exception:
            logger.exception('oper_log.response decode error')
        oper_log.status_code = response.status_code
        try:
            result_dict = json.loads(response.content)
            oper_log.c = result_dict['c']
            oper_log.m = result_dict['m']
        except Exception:
            oper_log.c = -1
            oper_log.m = u'返回非JSON格式'

    # 当服务器处理无任何返回结果时，记录响应、状态码、C、M
    else:
        oper_log.response = u'服务器处理无任何返回'
        oper_log.status_code = ''
        oper_log.c = -1
        oper_log.m = ''

    # DO SAVE
    oper_log.save()


def _is_need_log(request):
    if not request.path.startswith('/api/'):
        return False
    else:
        if request.path in EXCLUDE:
            return False
        else:
            return True


class Log2DBMiddleware(object):
    def process_request(self, request):
        self.request_time = datetime.datetime.now()

    def process_response(self, request, response):
        self.response_time = datetime.datetime.now()
        try:
            _save(request, self.request_time, self.response_time, response=response)
        except Exception as e:
            logger.exception('write db log fail!')
        finally:
            return response

    def process_exception(self, request, exception):
        self.response_time = datetime.datetime.now()
        try:
            _save(request, self.request_time, self.response_time, exception=exception)
        except Exception as e:
            logger.exception(e)
            logger.warn('write db log fail!')
        finally:
            logger.exception(exception)
            raise exception






