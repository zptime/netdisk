# -*- coding=utf-8 -*-

import logging

from applications.common.models import *
from applications.common.struct import struct_teacher, struct_student, struct_grade, struct_title
from utils.utils_tools import chinese2pinyin
from utils.utils_type import str2bool, bool2str
from utils.utils_user import student_qs

logger = logging.getLogger(__name__)


def setting_detail(key, school):
    qs = Setting.objects.filter(is_del=FALSE_INT, key=key, school=school)
    if not qs.exists():
        qs = Setting.objects.filter(is_del=FALSE_INT, key=key, school=None)
    if not qs.exists():
        value = SETTING_DEFAULT_DICT[key]
    else:
        value = qs.first().value
    return {
        'key': str(key),
        'value': str(value)
    }


def teacher_list(school, keyword, is_in, title):
    qs = Teacher.objects.filter(del_flag=FALSE_INT, school=school).select_related()
    # if is_in:
    #     qs = qs.filter(is_in=str2bool(str(is_in)))
    qs = qs.filter(is_in=True)
    if title:
        if title.name != u'班主任':
            qs = qs.filter(title=title)
        else:
            qs = qs.filter(cls__isnull=False)
    if keyword:
        qs = qs.filter(full_name__contains=keyword)
    raw_list = [struct_teacher(each) for each in qs]
    return sorted(raw_list, key=lambda x : chinese2pinyin(x['teacher_name']))


def student_list(school, keyword, grade_num, clazz):
    qs = student_qs(school=school).select_related()
    if keyword:
        qs = qs.filter(full_name__contains=keyword)
    if grade_num:
        clazzes = list(Class.objects.filter(del_flag=FALSE_INT, school=school, grade_num=grade_num))
        qs = qs.filter(cls__in=clazzes)
    if clazz:
        qs = qs.filter(cls=clazz)
    raw_list = [struct_student(each) for each in qs]
    return sorted(raw_list, key=lambda x: chinese2pinyin(x['student_name']))


def class_list(school):
    result = list()
    qs = Grade.objects.filter(del_flag=FALSE_INT, school=school).order_by('grade_num')
    for each_grade in qs:
        clazzes = list(Class.objects.filter(del_flag=FALSE_INT, school=school,
                        grade_name=each_grade.grade_name, grade_num=each_grade.grade_num))
        result.append(struct_grade(each_grade, clazzes))
    return result


def title_list(school):
    qs = Title.objects.filter(del_flag=FALSE_INT, school=school).order_by('type')
    return [struct_title(each) for each in qs]




