# -*- coding=utf-8 -*-

import calendar
import logging
import time
import datetime

from functools import wraps

from utils.const_def import *
from utils.const_err import *
from utils.utils_except import BusinessException

logger = logging.getLogger(__name__)


def record_time(func):
    """
        装饰器： 记录函数运行时间
    """
    @wraps(func)
    def returned_wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        return_value = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        logger.debug('runtime %s : %s' % (func.__name__, str(end_time - start_time)))
        return return_value
    return returned_wrapper


def is_today(date_str):
    """
    检查传入的日期是否为当天
    :param date_str:
    :return:
    """
    today_str = today(is_str=True)
    if date_str == today_str:
        return TRUE_STR

    return FALSE_STR


def today(FORMAT_DATE='%Y-%m-%d', is_str=True):
    """
        返回今天的时间
    """
    if is_str:
        return time.strftime(FORMAT_DATE, time.localtime(time.time()))
    else:
        return datetime.datetime.strptime(
            time.strftime(FORMAT_DATE, time.localtime(time.time())),
            FORMAT_DATE)


def tomorrow(FORMAT_DATE='%Y-%m-%d', is_str=True):
    """
        返回明天的时间
    """
    if is_str:
        return time.strftime(FORMAT_DATE, time.localtime(time.time() + 24 * 60 * 60))
    else:
        return datetime.datetime.strptime(
            time.strftime(FORMAT_DATE, time.localtime(time.time() + 24 * 60 * 60)),
            FORMAT_DATE)


def yesterday(FORMAT_DATE='%Y-%m-%d', is_str=True):
    """
        返回昨天的时间
    """
    if is_str:
        return time.strftime(FORMAT_DATE, time.localtime(time.time() - 24 * 60 * 60))
    else:
        return datetime.datetime.strptime(
            time.strftime(FORMAT_DATE, time.localtime(time.time() - 24 * 60 * 60)),
            FORMAT_DATE)


def now(FORMAT_DATETIME='%Y-%m-%d %H:%M:%S'):
    """
        获取当前时间：2013-09-10 11:22:11这样的时间年月日时分秒字符串
    """
    return time.strftime(FORMAT_DATETIME, time.localtime(time.time()))


def now_datetime():
    return datetime.datetime.now()


def datetime2str(datetime_para, format=TIME.DATE_STD):
    """
        时间转字符串
    """
    if not datetime_para:
        return ''
    return datetime_para.strftime(format)


def str2datetime(datetime_str, format=TIME.DATE_STD):
    """
        字符串转时间
    """
    try:
        day = datetime.datetime.strptime(datetime_str, format)
    except:
        day = None
    return day


def str2dt_DATE_STD(time_str, **kwargs):
    return str2datetime(time_str, format=TIME.DATE_STD)


def str2dt_DAY_STD(time_str, **kwargs):
    return str2datetime(time_str, format=TIME.DAY_STD)


def datetime2timestamp(dt, without_point=False):
    timeStamp = int(time.mktime(dt.timetuple()))
    timeStamp = '%.3f'% (float(str(timeStamp) + str("%06d" % dt.microsecond)) / 1000000)
    if without_point:
        timeStamp = timeStamp.replace('.', '')
    return timeStamp


def timestamp2datetime(ts):
    return datetime.datetime.fromtimestamp(ts)


def get_day_cycle(time_in, offset=0):
    """
    获取传入日期当天的开始结束时间
    :param time_in: 时间
    :param offset: 偏移量
    :return: 传入日期当天的开始结束时间
    """
    result = dict()
    date = time_in.date() + datetime.timedelta(days=offset)  # 日期不带时分秒
    result['startdate'] = datetime.datetime.combine(date, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(date, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(date + datetime.timedelta(days=1), datetime.time.min)
    return result


def get_week_cycle(time_in, offset=0):
    """
        获取本周的开始结束时间（周的概念为周一00:00:00到周日23:59:59）
        inparam: 时间，偏移量（周）  例如offset=0时，查询本周开始结束时间 ，为-1是查询上周开始结束时间
        outparam: {'startdate':startdate, 'enddate':enddate}
    """
    result = dict()
    week = time_in.weekday()  # 当前周数0-6 表示周一到周日
    date = time_in.date()  # 日期不带时分秒
    startdate = date + datetime.timedelta(days=(0-week+7*offset))
    enddate = date + datetime.timedelta(days=(6-week+7*offset))

    result['startdate'] = datetime.datetime.combine(startdate, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(enddate, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(enddate + datetime.timedelta(days=1), datetime.time.min)
    return result


def get_month_cycle(time_in, offset=0):
    """
    获取传入日期当月的开始结束时间
    :param time_in: 时间
    :param offset: 偏移量
    :return: 传入日期当月的开始结束时间
    """
    result = dict()
    date = time_in.date()

    weekday, last_day_num = calendar.monthrange(date.year, date.month)
    date_month_firstday = datetime.date(date.year, date.month, 1)
    date_month_lastday = datetime.date(date.year, date.month, last_day_num)

    # 获取offset个月前的月份
    for i in range(abs(offset)):
        if offset > 0:
            date = date_month_lastday + datetime.timedelta(days=1)
        elif offset < 0:
            date = date_month_firstday - datetime.timedelta(days=1)
        else:
            break

        weekday, last_day_num = calendar.monthrange(date.year, date.month)
        date_month_firstday = datetime.date(date.year, date.month, 1)
        date_month_lastday = datetime.date(date.year, date.month, last_day_num)

    result['startdate'] = datetime.datetime.combine(date_month_firstday, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(date_month_lastday, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(date_month_lastday + datetime.timedelta(days=1), datetime.time.min)

    return result


def get_season_cycle(time_in, offset=0):
    """
    获取传入日期当季度的开始结束时间(一季度为1到3月，二季度为4到6月，三季度为7到9月，二季度为10到12月，)
    :param time_in: 时间
    :param offset: 偏移量
    :return: 传入日期当季度的开始结束时间
    """
    result = dict()
    termlist = [
        {'termid': 1, 'startmonth': 1, 'endmonth': 3},
        {'termid': 2, 'startmonth': 4, 'endmonth': 6},
        {'termid': 3, 'startmonth': 7, 'endmonth': 9},
        {'termid': 4, 'startmonth': 10, 'endmonth': 12},
    ]
    curterm = (time_in.month - 1) / 3 + 1
    queryterm = (curterm + offset - 1) % 4 + 1
    queryyear = time_in.year + int((curterm + offset - 1)/4)

    querystartmonth = termlist[queryterm-1]['startmonth']
    queryendmonth = termlist[queryterm-1]['endmonth']

    weekday, last_day_num = calendar.monthrange(queryyear, queryendmonth)

    startdate = datetime.datetime.strptime("%d-%d-1" % (queryyear, querystartmonth), "%Y-%m-%d")
    enddate = datetime.datetime.strptime("%d-%d-%d" % (queryyear, queryendmonth, last_day_num), "%Y-%m-%d")

    result['startdate'] = datetime.datetime.combine(startdate, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(enddate, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(enddate + datetime.timedelta(days=1), datetime.time.min)

    return result


def get_term_cycle(time_in, offset=0):
    """
    获取传入日期当学期的开始结束时间(上半学年为上次9月1日0点0分0秒到之后的第一个1月31日23点59分59秒，下半学年为2月1日到下次8月31日23点59分59秒)
    :param time_in: 时间
    :param offset: 偏移量
    :return: 传入日期当学期的开始结束时间
    """
    # 查询传入的时间是第几学期，起止于哪年
    result = dict()
    if time_in.month >= 9:
        startyear = time_in.year + (offset+1)/2
        firstudyyear = True
    elif time_in.month < 2:
        startyear = time_in.year - 1 + (offset+1)/2
        firstudyyear = True
    else:
        startyear = time_in.year + offset/2
        firstudyyear = False

    if offset % 2 != 0:
        firstudyyear = not firstudyyear

    # 根据学期和年份获取起止时间
    if firstudyyear:
        endyear = startyear + 1
        startdate = datetime.datetime.strptime("%s-9-1" % startyear, "%Y-%m-%d")
        enddate = datetime.datetime.strptime("%s-1-31" % endyear, "%Y-%m-%d")
    else:
        endyear = startyear
        startdate = datetime.datetime.strptime("%s-2-1" % startyear, "%Y-%m-%d")
        enddate = datetime.datetime.strptime("%s-8-31" % endyear, "%Y-%m-%d")

    result['startdate'] = datetime.datetime.combine(startdate, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(enddate, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(enddate + datetime.timedelta(days=1), datetime.time.min)
    return result


def get_year_cycle(time_in, offset=0):
    """
    获取传入日期当年的开始结束时间（当年时间为上次1月1日0点0分0秒到下次12月31日23点59分59秒）
    :param time_in: 时间
    :param offset: 偏移量
    :return: 传入日期当年的开始结束时间
    """
    result = dict()
    year = time_in.year + offset
    startdate = datetime.datetime.strptime("%s-1-1" % year, "%Y-%m-%d")
    enddate = datetime.datetime.strptime("%s-12-31" % year, "%Y-%m-%d")

    result['startdate'] = datetime.datetime.combine(startdate, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(enddate, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(enddate + datetime.timedelta(days=1), datetime.time.min)
    return result


def get_schoolyear_cycle(time_in, offset=0):
    """
    获取传入日期当学年的开始结束时间，（学年时间为上次9月1日0点0分0秒到下次8月30日23点59分59秒）
    :param time_in: 时间
    :param offset: 偏移量
    :return: 传入日期当学年的开始结束时间
    """
    result = dict()
    if time_in.month >= 9:
        year = time_in.year + offset
    else:
        year = time_in.year - 1 + offset
    nextyear = year + 1

    startdate = datetime.datetime.strptime("%s-9-1" % year, "%Y-%m-%d")
    enddate = datetime.datetime.strptime("%s-8-31" % nextyear, "%Y-%m-%d")

    result['startdate'] = datetime.datetime.combine(startdate, datetime.time.min)
    result['enddate'] = datetime.datetime.combine(enddate, datetime.time.max)
    result['enddate_pro'] = datetime.datetime.combine(enddate + datetime.timedelta(days=1), datetime.time.min)
    return result


def get_unify_time(timestr):
    """
    将时间格式统一转换为时间格式，
    支持时间2017-02-28或2017-02-28 08:58:18或python时间戳1488767197或java时间戳1488767197123
    :param timestr:时间字符串，格式如上
    :return:%Y-%m-%d %H:%M:%S格式的时间字符串
    """
    # 检查传入的是时间戳还是时间，如果是时间戳则自动转换为时间
    if timestr.find('-') < 0:
        if len(timestr) == 13:
            result = datetime.datetime.fromtimestamp(float(timestr) / 1000)
        else:
            result = datetime.datetime.fromtimestamp(float(timestr))
    else:
        if timestr.find(':') < 0:
            result = datetime.datetime.strptime(timestr, "%Y-%m-%d")
        else:
            result = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

    return result


def get_time_perform(timestr):
    """
    将timestr转换为前端可以展示的时间
    :param timestr: %Y-%m-%d %H:%M:%S
    :return: %Y-%m-%d %H:%M，当天显示为“今天 %H:%M”，昨天显示为“昨天 %H:%M”
    """
    if not timestr:
        return ''

    in_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    in_date = datetime.datetime.combine(in_datetime, datetime.time.min)
    in_date_str = in_date.strftime("%Y-%m-%d")
    in_time_str = in_datetime.strftime("%H:%M")

    today_datetime = datetime.datetime.now()
    today_date = datetime.datetime.combine(today_datetime, datetime.time.min)
    yestody_date = today_date - datetime.timedelta(days=1)

    if in_date == today_date:
        out_date = '今天'
    elif in_date == yestody_date:
        out_date = '昨天'
    else:
        out_date = in_date_str

    result = out_date + ' ' + in_time_str

    return result


def get_datetypelist_daterange(startdate, enddate, datetype):
    """
    通过时间范围获取对应的日期类型列表
    例如：
    传入时间
    入参:日期:时间格式，非字符串格式
         时间类型：天MEDAL_DATE_TYPE_DAY、周MEDAL_DATE_TYPE_WEEK、月MEDAL_DATE_TYPE_MONTH
    出参：[{序号，时间类型，开始时间，结束时间}]
        时间列表，字符串格式%Y-%m-%d %H:%M:%S
    """
    result = list()
    ordersn = 1  # 序号
    datetemp = datetime.datetime.combine(startdate, datetime.time.min)

    if datetype == DATE_TYPE_DAY:
        while True:
            if enddate < datetemp:
                break

            result_row = dict()
            result_row['order'] = ordersn
            result_row['datetype'] = DATE_TYPE_DAY
            result_row['startdate'] = datetime.datetime.combine(datetemp, datetime.time.min)
            result_row['enddate'] = datetime.datetime.combine(datetemp, datetime.time.max)
            result_row['enddate_pro'] = datetime.datetime.combine(datetemp + datetime.timedelta(days=1), datetime.time.min)
            result.append(result_row)

            datetemp += datetime.timedelta(days=1)
            ordersn += 1
    elif datetype == DATE_TYPE_WEEK:  # 注意：此处查出来的周有可能跨月。
        while True:
            if enddate < datetemp:
                break
            result_row = dict()
            result_row['order'] = ordersn
            result_row['datetype'] = DATE_TYPE_MONTH
            weekcycle = get_week_cycle(datetemp)
            result_row['startdate'] = weekcycle['startdate']
            result_row['enddate'] = weekcycle['enddate']
            result_row['enddate_pro'] = weekcycle['enddate_pro']
            result.append(result_row)

            datetemp += datetime.timedelta(days=7)
            ordersn += 1
    elif datetype == DATE_TYPE_MONTH:
        while True:
            if enddate < datetemp:
                break
            result_row = dict()
            result_row['order'] = ordersn
            result_row['datetype'] = DATE_TYPE_MONTH
            monthcycle = get_month_cycle(datetemp)
            result_row['startdate'] = monthcycle['startdate']
            result_row['enddate'] = monthcycle['enddate']
            result_row['enddate_pro'] = monthcycle['enddate_pro']
            result.append(result_row)

            datetemp = get_nextmonth_firstday(datetemp)
            ordersn += 1

    else:
        raise BusinessException(WRONG_TIME_TYPE)

    return result


def get_nextmonth_firstday(time_in):
    """
    获取下月1日时间
    :param time_in: 时间，时间格式
    :return:时间，时间格式
    """
    # 先获取本月1号
    indate_firstday = datetime.datetime.strptime("%d-%d-1" % (time_in.year, time_in.month), "%Y-%m-%d")

    # 本月1号+32天一定是下月
    outdate = indate_firstday + datetime.timedelta(days=32)
    outdate_firstday = datetime.datetime.strptime("%d-%d-1" % (outdate.year, outdate.month), "%Y-%m-%d")

    return outdate_firstday


def get_day_list(startdate, enddate):
    """
    将时间范围转为按天的时间列表，时间均为日期格式
    :param startdate:
    :param enddate:
    :return: 日期格式列表
    """
    result = list()
    if startdate > enddate:
        raise BusinessException(PARAM_ERROR_LARGE_STARTDATE)

    # 转成只带日期的时间格式
    startdate = datetime.datetime.strptime(startdate.strftime("%Y-%m-%d"), "%Y-%m-%d")
    enddate = datetime.datetime.strptime(enddate.strftime("%Y-%m-%d"), "%Y-%m-%d")

    datetmp = startdate
    while datetmp <= enddate:
        result.append(datetmp)
        datetmp = datetmp + datetime.timedelta(days=1)

    return result


def get_cycletime_from_date_type(date_type, startdate=None, enddate=None, offset=0):
    """
        将时段类型转换为开始结束时间
    """
    result = dict()
    if date_type:
        date_type = int(date_type)
        if date_type == DATE_TYPE_STUDYYEAR:
            result = get_schoolyear_cycle(datetime.datetime.now(), offset)
        elif date_type == DATE_TYPE_TODAY:
            result = get_day_cycle(datetime.datetime.now(), offset)
        elif date_type == DATE_TYPE_THISWEEK:
            result = get_week_cycle(datetime.datetime.now(), offset)
        elif date_type == DATE_TYPE_THISMONTH:
            result = get_month_cycle(datetime.datetime.now(), offset)
        elif date_type == DATE_TYPE_LASTMONTH:
            result = get_month_cycle(datetime.datetime.now(), offset-1)
        elif date_type == DATE_TYPE_THISSEASON:
            result = get_season_cycle(datetime.datetime.now(), offset)
        elif date_type == DATE_TYPE_THISTERM:
            result = get_term_cycle(datetime.datetime.now(), offset)
        elif date_type == DATE_TYPE_THISSCHOOLYEAR:
            result = get_schoolyear_cycle(datetime.datetime.now(), offset)
        else:
            raise BusinessException(DATETYPE_ERR)
    else:
        if not startdate or not enddate:
            raise BusinessException(REQUEST_PARAM_ERROR)

        result['startdate'] = get_unify_time(startdate)
        result['enddate'] = get_unify_time(enddate)
        result['enddate_pro'] = result['enddate']
    return result


def is_future_time(time_dt, delta=0):
    return time_dt > (now_datetime() + datetime.timedelta(days=delta))


