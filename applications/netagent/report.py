# coding=utf-8
import logging
import os

from applications.bizlog.models import OperateLog
from applications.netagent.netrequest import uploadlog
from utils.const_def import TRUE_INT
from utils.utils_time import yesterday, today
from django.conf import settings

from utils.utils_time import datetime2str

SEND_APPENDIX_SIZE_MAX = 1024 * 1024 * 8  # 8MB
LONG_REQUEST = 1000 * 2  # 2s
logger = logging.getLogger(__name__)


def request_long(report):
    # http长请求数(>2s,不含上传操作)
    exclude_oper = ['api_upload_image', 'api_upload_video', 'api_upload_voice', 'api_upload_file', ]
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    qs = OperateLog.objects.filter(
        request_time__gte=yesterday_dt, request_time__lt=today_dt, duration__gte=LONG_REQUEST) \
        .exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None)
    lines = list()
    report.writelines(['\n[http长请求(>2s, 不含上传操作)]: \n', ])
    for each in qs:
        lines.append(u'ID:%d, url:%s, 时长:%d, 请求者:%d_%d_%d, 响应码:%s, c:%s, m:%s, 时间:%s\n'
            % (each.id, each.url, each.duration, each.account_id, each.user_type,
               each.user_school_id, each.status_code, each.c, each.m, datetime2str(each.request_time)))
    report.writelines(lines)
    return len(lines)


def request_200_with_error(report):
    # http请求"200"且包含非0内部状态码响应数
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    qs = OperateLog.objects\
        .filter(request_time__gte=yesterday_dt, request_time__lt=today_dt, status_code='200')\
        .exclude(c=0).exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None)
    lines = list()
    report.writelines(['\n[http请求"200"且包含非0内部状态码响应]: \n', ])
    for each in qs:
        lines.append(u'ID:%d, url:%s, 请求者:%d_%d_%d, c:%s, m:%s, 时间:%s\n'
            % (each.id, each.url, each.account_id, each.user_type,
               each.user_school_id, each.c, each.m, datetime2str(each.request_time)))
    report.writelines(lines)
    return len(lines)


def request_non_200(report):
    # http请求"非200"响应数, 详情见邮件附件
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    qs = OperateLog.objects.filter(
        request_time__gte=yesterday_dt, request_time__lt=today_dt).exclude(status_code='200') \
        .exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None)
    lines = list()
    report.writelines(['\n[http请求"非200"响应]: \n', ])
    for each in qs:
        lines.append(u'ID:%d, url:%s, 请求者:%d_%d_%d, 响应码:%s, c:%s, m:%s, 时间:%s\n'
            % (each.id, each.url, each.account_id, each.user_type, each.user_school_id,
               each.status_code, each.c, each.m, datetime2str(each.request_time)))
    report.writelines(str(lines))
    return len(lines)


def request_500(report):
    # http请求"500"响应数, 详情见邮件附件
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    qs = OperateLog.objects.filter(
        request_time__gte=yesterday_dt, request_time__lt=today_dt, status_code='500') \
        .exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None)
    lines = list()
    report.writelines(['\n[http请求"500"响应]: \n', ])
    for each in qs:
        lines.append(u'ID:%d, url:%s, 请求者:%d_%d_%d, c:%s, m:%s, 时间:%s\n'
            % (each.id, each.url, each.account_id, each.user_type,
               each.user_school_id, each.c, each.m, datetime2str(each.request_time)))
    report.writelines(lines)
    return len(lines)


def total_request_unsafe():
    # http非安全操作请求数
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    result = OperateLog.objects.filter(
        request_time__gte=yesterday_dt, request_time__lt=today_dt) \
        .exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None) \
        .count()
    return result


def total_request():
    # http所有请求数
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    result = OperateLog.objects.filter(request_time__gte=yesterday_dt, request_time__lt=today_dt) \
        .exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None) \
        .count()
    return result


def total_user():
    # 总使用人数
    today_dt = today(is_str=False)
    yesterday_dt = yesterday(is_str=False)
    result = OperateLog.objects.filter(request_time__gte=yesterday_dt, request_time__lt=today_dt) \
        .exclude(account_id=None).exclude(user_type=None).exclude(user_school_id=None) \
        .values_list("account_id", flat=True).distinct().count()
    return result


def daily_report():
    report_path = os.path.join(settings.BASE_DIR, 'temp', 'report_%s_%s.log' % (yesterday(), settings.SYSTEM_DESC))
    mail_title = u'昨日(%s)%s运行情况' % (yesterday(), settings.SYSTEM_DESC)
    mail_content = mail_title + '\n\n'

    with open(report_path, 'w+') as report:
        # 前一天总用户数
        totaluser = total_user()

        # 前一天总http请求数
        totalrequest = total_request()

        # 前一天总http请求数(非安全操作)
        totalrequestunsafe = total_request_unsafe()

        # http请求非200响应
        requestnon200 = request_non_200(report)

        # http请求500响应
        request500 = request_500(report)

        # http请求"200"且包含非0内部状态码
        request200witherror = request_200_with_error(report)

        # http长请求
        requestlong = request_long(report)

        # 日志中异常ERROR数量
        reportlogerror = report_log_error(report)

    send_mail(mail_title, mail_content, report_path, totaluser, totalrequest, totalrequestunsafe, requestnon200, request500, request200witherror, requestlong, reportlogerror, '', '', yesterday())


def send_mail(mail_title, mail_content, report_path, totaluser, totalrequest, totalrequestunsafe, requestnon200, request500, request200witherror, requestlong, reportlogerror, desription1, desription2, cycle_time):
    try:
        uploadlog(report_path, totaluser, totalrequest, totalrequestunsafe, requestnon200, request500, request200witherror, requestlong, reportlogerror, desription1, desription2, cycle_time)
        # send_appendix = True if os.path.getsize(report_path) <= SEND_APPENDIX_SIZE_MAX else False
        # if not send_appendix:
        #     mail_content += u'\n附件超过限制大小(8MB)，请在项目temp路径下查看\n'
        # email = EmailMessage(
        #     mail_title,
        #     mail_content,
        #     settings.EMAIL_HOST_USER,
        #     settings.EMAIL_SENDTO,
        #     [])
        # if send_appendix:
        #     email.attach_file(report_path)
        # email.send()
    except Exception as e:
        logger.exception('send daily report email fail')


def report_log_error(report_file):
    # django日志文件中ERROR个数
    def _report_single_log_error(log_path, report_file):
        inner_count = 0
        yesterday_str = yesterday()
        with open(log_path, 'r') as f:
            err_bucket = list()
            err_flag = False
            for line in f:
                if line.startswith(yesterday_str):
                    if err_flag:
                        report_file.writelines(err_bucket)
                        err_flag = False
                        err_bucket[:] = []
                    if '[ERROR]' in line:
                        inner_count += 1
                        err_flag = True
                        err_bucket.append(line)
                else:
                    if err_flag:
                        err_bucket.append(line)
        return inner_count
    count = 0
    report_file.writelines(['\n[django日志文件中ERROR]: \n',])
    (shortname, extension) = os.path.splitext(get_django_log_path())
    LOG_PATH_DJANGO_ROTATE_1 = shortname + '.1' + extension
    if os.path.exists(LOG_PATH_DJANGO_ROTATE_1):
        count += _report_single_log_error(LOG_PATH_DJANGO_ROTATE_1, report_file)
    count += _report_single_log_error(get_django_log_path(), report_file)
    return count


def get_django_log_path():
    # 查询日志目录，先找LOGGING的配置,找不到则取settings.LOG_PATH_DJANGO配置 ，如果仍找不到，则默认取log/django.log
    try:
        logpath = settings.LOGGING['handlers']['default']['filename']
    except:
        if hasattr(settings, 'LOG_PATH_DJANGO') and settings.LOG_PATH_DJANGO:
            logpath = settings.LOG_PATH_DJANGO
        else:
            logpath = os.path.join(settings.BASE_DIR + '/log/', 'django.log')
    return logpath
