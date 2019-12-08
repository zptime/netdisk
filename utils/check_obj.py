# -*- coding: utf-8 -*-

import logging

from django.conf import settings

from utils.const_def import *
from utils.const_err import *
from utils.utils_except import BusinessException
from utils.utils_user import get_user

from applications import common
from applications.user_center.models import *


logger = logging.getLogger(__name__)


def check_get_account(account_id):
    if not account_id:
        raise BusinessException(USER_NOT_EXIST)
    account = Account.objects.filter(id=int(account_id), del_flag=FALSE_INT).first()
    if not account:
        raise BusinessException(USER_NOT_EXIST)
    return account


def check_get_school(school_id):
    if not school_id:
        raise BusinessException(SCHOOl_NOT_EXIST)
    school = School.objects.filter(id=int(school_id), del_flag=FALSE_INT).first()
    if not school:
        raise BusinessException(SCHOOl_NOT_EXIST)
    return school


def check_get_class(class_id):
    if not class_id:
        raise BusinessException(CLASS_NOT_EXIST)
    clazz = Class.objects.filter(id=int(class_id), del_flag=FALSE_INT).first()
    if not clazz:
        raise BusinessException(CLASS_NOT_EXIST)
    return clazz


def check_get_teacher(teacher_id):
    if not teacher_id:
        raise BusinessException(TEACHER_NOT_EXIST)
    teacher = Teacher.objects.filter(id=int(teacher_id), del_flag=FALSE_INT).first()
    if not teacher:
        raise BusinessException(TEACHER_NOT_EXIST)
    return teacher


def check_get_teacher_by_request(request):
    user_type = request.user.type   # int
    school_id = request.user.school.id   # int
    account_id = request.user.id   # int
    if user_type != USER_TYPE_TEACHER:
        raise BusinessException(TEACHER_NOT_EXIST)
    teacher = get_user(account_id, user_type, school_id)
    if not teacher:
        raise BusinessException(TEACHER_NOT_EXIST)
    return teacher


def check_get_parent(parent_id):
    if not parent_id:
        raise BusinessException(PARENT_NOT_EXIST)
    parent = Parent.objects.filter(id=int(parent_id), del_flag=FALSE_INT).first()
    if not parent:
        raise BusinessException(PARENT_NOT_EXIST)
    return parent


def check_get_student(student_id):
    if not student_id:
        raise BusinessException(STUDENT_NOT_EXIST)
    student = Student.objects.filter(id=int(student_id), del_flag=FALSE_INT).first()
    if not student:
        raise BusinessException(STUDENT_NOT_EXIST)
    return student


def check_get_title(title_id, user=None):
    if not title_id:
        raise BusinessException(TITLE_NOT_EXIST)
    qs = Title.objects.filter(id=int(title_id), del_flag=FALSE_INT)
    if user:
        qs = qs.filter(school=user.school)
    title = qs.first()
    if not title:
        raise BusinessException(TITLE_NOT_EXIST)
    return title


def check_get_grade(grade_id, user=None):
    if not grade_id:
        raise BusinessException(GRADE_NOT_EXIST)
    qs = Grade.objects.filter(id=int(grade_id), del_flag=FALSE_INT)
    if user:
        qs = qs.filter(school=user.school)
    grade = qs.first()
    if not grade:
        raise BusinessException(GRADE_NOT_EXIST)
    return grade


def check_get_clazz(clazz_id, user=None):
    if not clazz_id:
        raise BusinessException(CLASS_NOT_EXIST)
    qs = Class.objects.filter(id=int(clazz_id), del_flag=FALSE_INT)
    if user:
        qs = qs.filter(school=user.school)
    clazz = qs.first()
    if not clazz:
        raise BusinessException(CLASS_NOT_EXIST)
    return clazz

