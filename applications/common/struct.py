# -*- coding=utf-8 -*-

import logging

from utils.const_err import *
from utils.const_def import *

from utils.net_helper import url_with_uc_domain
from utils.utils_time import datetime2str
from utils.utils_type import bool2str


logger = logging.getLogger(__name__)


def struct_school(school):
    result = collections.OrderedDict()
    result['school_id'] = str(school.id) if school else ''
    result['school_name'] = str(school.name_full) if school else ''
    result['school_code'] = school.code if school else ''
    return result


def struct_title(title, prefix='teacher_'):
    result = collections.OrderedDict()
    result['%stitle_id' % prefix] = str(title.id) if title else ''
    result['%stitle_name' % prefix] = title.name if title else ''
    return result


def struct_grade(grade, clazzes):
    result = collections.OrderedDict()
    result['grade_id'] = str(grade.id) if grade else ''
    result['grade_num'] = str(grade.grade_num) if grade else ''
    result['grade_name'] = grade.grade_name if grade else ''

    clazzes = clazzes or list()
    result['grade_clazz_list'] = [struct_clazz(each) for each in clazzes]

    # school = grade.school if grade else None
    # result.update(struct_school(school))
    return result


def struct_clazz(clazz, prefix='clazz_'):
    result = collections.OrderedDict()
    result['%sid' % prefix] = str(clazz.id) if clazz else ''
    result['%sname' % prefix] = clazz.class_name if clazz else ''
    result['%snum' % prefix] = str(clazz.class_num) if clazz else ''
    result['%sgrade_name' % prefix] = clazz.grade_name if clazz else ''
    result['%sgrade_num' % prefix] = str(clazz.grade_num) if clazz else ''
    result['%sis_graduate' % prefix] = str(clazz.graduate_status) if clazz else ''
    result['%salias' % prefix] = clazz.class_alias if clazz else ''
    return result


def struct_teacher(teacher, prefix='teacher_'):
    result = collections.OrderedDict()
    result['%sid' % prefix] = str(teacher.id) if teacher else ''
    result['%saccount_id' % prefix] = str(teacher.account.id) if teacher else ''
    result['%sname' % prefix] = teacher.full_name if teacher else ''
    result['%savatar' % prefix] = url_with_uc_domain(teacher.image_url) if teacher else ''
    result['%ssex' % prefix] = teacher.sex if teacher else ''
    # result['%sphone' % prefix] = teacher.account.mobile if teacher else ''
    result['%sidcard' % prefix] = teacher.id_card if teacher else ''
    result['%sworkcard' % prefix] = teacher.school_code if teacher else ''
    result['%sworkcard_tmp' % prefix] = teacher.tmp_code if teacher else ''
    result['%sis_in' % prefix] = bool2str(teacher.is_in) if teacher else ''
    # result['%sin_date' % prefix] = datetime2str(teacher.in_date) if teacher else ''
    # result['%sout_date' % prefix] = datetime2str(teacher.out_date) if teacher else ''

    title = teacher.title if teacher else None
    result.update(struct_title(title, prefix=prefix))

    school = teacher.school if teacher else None
    result.update(struct_school(school))

    # clazz = teacher.cls if teacher else None
    # result.update(struct_clazz(clazz, prefix='managed_clazz_'))

    return result


def struct_student(student):
    result = collections.OrderedDict()
    result['student_id'] = str(student.id) if student else ''
    result['student_account_id'] = str(student.account.id) if student else ''
    result['student_name'] = student.full_name if student else ''
    result['student_avatar'] = url_with_uc_domain(student.image_url) if student else ''
    result['student_sex'] = student.sex if student else ''
    # result['student_phone'] = student.account.id if student else ''
    result['student_idcard'] = student.id_card if student else ''
    # result['student_study_code'] = student.account.code if student else ''
    result['student_is_in'] = bool2str(student.is_in) if student else ''
    # result['student_entry_date'] = datetime2str(student.entry_date) if student else ''
    # result['student_out_date'] = datetime2str(student.out_date) if student else ''

    school = student.school if student else None
    result.update(struct_school(school))

    # clazz = student.cls if student else None
    # result.update(struct_clazz(clazz))

    return result
