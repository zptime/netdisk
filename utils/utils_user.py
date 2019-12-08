# -*- coding=utf-8 -*-

import logging

import datetime
from applications.user_center.models import *
from utils.const_def import *
from utils.const_err import *
from utils.net_helper import url_with_uc_domain
from utils.utils_except import BusinessException
from utils.utils_time import now_datetime

logger = logging.getLogger(__name__)


def get_user(account_id, user_type, school_id, restrict_mode=True):
    qs = None
    if int(user_type) == USER_TYPE_STUDENT:
        qs = Student.objects.filter(
            account_id=int(account_id), account__del_flag=FALSE_INT, school_id=int(school_id), school__del_flag=FALSE_INT, del_flag=FALSE_INT)
        if restrict_mode:
            qs = qs.filter(is_in=TRUE_INT, cls__graduate_status=FALSE_INT)
    elif int(user_type) == USER_TYPE_TEACHER:
        qs = Teacher.objects.filter(
            account_id=int(account_id), account__del_flag=FALSE_INT, school_id=int(school_id), school__del_flag=FALSE_INT, del_flag=FALSE_INT)
        if restrict_mode:
            qs = qs.filter(is_in=True)
    elif int(user_type) == USER_TYPE_PARENT:
        qs = Parent.objects.filter(account_id=int(account_id), account__del_flag=FALSE_INT,
            school_id=int(school_id), school__del_flag=FALSE_INT, is_active=TRUE_INT, del_flag=FALSE_INT)
        if restrict_mode:
            relation = ParentStudent.objects.filter(del_flag=FALSE_INT)
            school = School.objects.get(pk=int(school_id))
            qs = qs.filter(parentstudent__in=relation, parentstudent__status=APPLICATION_STATUS_APPROVED[0],
                           parentstudent__student__in=student_qs(school=school).all()).distinct()
    return qs.first() if qs else None


def student_qs(school=None, only_in=True, only_normal=False, only_not_graduate=True):
    qs = Student.objects.filter(del_flag=FALSE_INT)
    if only_in:
        qs = qs.filter(is_in=TRUE_INT)
    if school:
        qs = qs.filter(school=school)
    if only_normal:
        qs = qs.filter(kind=u'正常')
    if only_not_graduate:
        qs = qs.filter(cls__graduate_status=FALSE_INT)
    return qs


def parent_qs(school=None, only_active=True, only_with_child=True):
    relation = ParentStudent.objects.filter(del_flag=FALSE_INT)
    qs = Parent.objects.filter(del_flag=FALSE_INT)
    if school:
        qs = qs.filter(school=school)
    if only_active:
        qs = qs.filter(is_active=TRUE_INT)
    if only_with_child:
        qs = qs.filter(parentstudent__in=relation, parentstudent__status=APPLICATION_STATUS_APPROVED[0],
                       parentstudent__student__in=student_qs(school=school).all()).distinct()
    return qs


"""
{ 
  'account_id,user_type,school_id':
  {
      'expire_time': dt,
      'userinfo': {
          full_name: xxx
          avatar: url
          role_id: xxx
      }
  }
}
"""
USERINFO_CACHE = dict()
USERINFO_CACHE_EXPIRED_HOURS = 24


def get_userinfo_from_cache(account_id, user_type, school_id):
    global USERINFO_CACHE
    key = '%s_%s_%s' % (account_id, user_type, school_id)
    if key in USERINFO_CACHE and USERINFO_CACHE[key]['expire_time'] > now_datetime():
        return USERINFO_CACHE[key]['userinfo']
    else:
        role = get_user(account_id, user_type, school_id)
        avatar = url_with_uc_domain(role.image_url) if role else ''
        USERINFO_CACHE[key] = {
            'expire_time': now_datetime() + datetime.timedelta(hours=USERINFO_CACHE_EXPIRED_HOURS),
            'userinfo': {
                'full_name': role.full_name if role else '',
                'avatar': avatar,
                'role_id': str(role.id) if role else '',
            }
        }
        return USERINFO_CACHE[key]['userinfo']





