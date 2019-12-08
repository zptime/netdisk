# -*- coding: utf-8 -*-

import logging
import types
from functools import wraps

from django.conf import settings

from utils.const_err import *
from utils.const_def import *
from utils.net_helper import response405, response403, response200, response400
from utils.net_subnet import is_internal_request
from utils.utils_except import BusinessException
from utils.utils_user import get_user

from applications import common
from applications.user_center.models import *


logger = logging.getLogger(__name__)


def is_admin(request):
    return is_admin_by_user(request.user)


def is_admin_by_user(user):
    teacher = get_user(user.id, user.type, user.school.id)
    if not isinstance(teacher, Teacher):
        return False
    current_services = Service.objects.filter(code__in=settings.SYSTEM_SERVICES, del_flag=FALSE_INT)
    super_role = Role.objects.filter(service__in=current_services, code=SUPER_ADMIN_CODE, del_flag=FALSE_INT).first()
    return UserRole.objects.filter(user=teacher, school=teacher.school, role=super_role, del_flag=FALSE_INT).exists()


def validate(method, para=None, internal=False, auth=True,
                usertype=(USER_TYPE_STUDENT, USER_TYPE_TEACHER, USER_TYPE_PARENT), conditions=None):
    """
        'para' setting:
            - mandatory: name      表单字段名称
            - optional:  default   为空时的默认值，配置此字段则表示支持为空(None或'')
                         convert   转换器
                         file      文件类型
    """
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            # 请求GET / POST校验
            if request.method != method:
                return response405({'c': REQUEST_WRONG_METHOD[0], 'm': REQUEST_WRONG_METHOD[1]})
            # 内部请求校验
            if internal:
                if not is_internal_request(request):
                    return response403({'c': REQUEST_INTERNAL[0], 'm': REQUEST_INTERNAL[1]})
            else:
                if auth:
                    if request.user.username == settings.DB_ADMIN:
                        return response403({'c': ROOT_FORBID[0], 'm': ROOT_FORBID[1]})
                    if not request.user.is_authenticated():
                        return response200({'c': AUTH_NEED_LOGIN[0], 'm': AUTH_NEED_LOGIN[1]})

                    # 检查用户是否存在
                    if not get_user(request.user.id, request.user.type, request.user.school.id, restrict_mode=False):
                        return response403({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})

                    # 检查用户所在学校是否启用了该服务
                    services_avai_count = request.user.school.schoolservice_set \
                        .filter(service__code__in=settings.SYSTEM_SERVICES,
                                del_flag=FALSE_INT,
                                service__del_flag=FALSE_INT,
                                school__del_flag=FALSE_INT) \
                        .count()
                    if services_avai_count <= 0:
                        return response403({'c': AUTH_WRONG_SCHOOL[0], 'm': AUTH_WRONG_SCHOOL[1]})

                    # 检查HTTP请求头，是否用户类型已经被PC端切换
                    mobile_user_head = request.META.get('HTTP_' + settings.HTTP_HEADER_CURRENT_USER_TYPE, '')
                    if mobile_user_head:  # 该请求头可选
                        mobile_user_type = mobile_user_head.split(',')[0]
                        mobile_school_id = mobile_user_head.split(',')[1]
                        if request.user.type != int(mobile_user_type) or request.user.school.id != int(mobile_school_id):
                            return response403({'c': AUTH_USER_TYPE_CRUSH[0], 'm': AUTH_USER_TYPE_CRUSH[1]})

                    # 检查用户类型是否被允许
                    if request.user.type not in usertype:
                        return response403({'c': AUTH_WRONG_TYPE[0], 'm': AUTH_WRONG_TYPE[1]})
                    else:
                        # e.g. conditions=foo
                        # e.g. conditions=('AND', (foo1, foo2, foo3))
                        # e.g. conditions=('OR', (foo1, foo2, foo3))
                        if not conditions:
                            pass
                        elif isinstance(conditions, tuple):
                            if conditions[0] == 'AND':
                                for condition in conditions[1]:
                                    if not isinstance(condition, types.FunctionType):
                                        continue
                                    if not condition(request):
                                        return response403({'c': AUTH_CONDITION_FAIL[0], 'm': AUTH_CONDITION_FAIL[1]})
                            if conditions[0] == 'OR':
                                result = False
                                for condition in conditions[1]:
                                    if not isinstance(condition, types.FunctionType):
                                        continue
                                    if condition(request):
                                        result = True
                                        break
                                if not result:
                                    return response403({'c': AUTH_CONDITION_FAIL[0], 'm': AUTH_CONDITION_FAIL[1]})
                        elif isinstance(conditions, types.FunctionType):
                            if not conditions(request):
                                return response403({'c': AUTH_CONDITION_FAIL[0], 'm': AUTH_CONDITION_FAIL[1]})
                        else:
                            pass
                else:
                    pass

            # 进行基本参数校验
            if para:
                para_dict = collections.OrderedDict()
                for each in para:
                    if method == 'GET':
                        raw_para = request.GET.get(each['name'])
                    elif method == 'POST':
                        if each.get('is_file', False):
                            raw_para = request.FILES.get(each['name'])
                            # ext = raw_para.name[raw_para.name.rfind('.') + 1:]
                            # if ('*' not in each['file'].EXT) and (ext.lower() not in each['file'].EXT):
                            #     return response400({"c": REQUEST_PARAM_ERROR[0], "m": u'文件格式不支持'})
                            # if raw_para.size > each['file'].SIZE:
                            #     return response400({"c": REQUEST_PARAM_ERROR[0], "m": u'文件大小超出限制'})
                        else:
                            raw_para = request.POST.get(each['name'])
                    else:
                        return response400({"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1]})
                    if not raw_para:
                        if not 'default' in each.keys():
                            msg = REQUEST_PARAM_ERROR[1] + u': 请求参数[%s]不能为空' % each['name']
                            return response400({"c": REQUEST_PARAM_ERROR[0], "m": msg})
                        else:
                            raw_para = each.get('default', '')
                    convert_method = each.get('convert')
                    if convert_method and callable(convert_method):
                        key = each['name']
                        if each['name'].endswith('_id'):
                            key = key[0:-3]
                        if not raw_para:
                            para_dict[key] = None
                        else:
                            try:
                                convertted = convert_method(raw_para, user=request.user)
                            except BusinessException as be:
                                msg = REQUEST_PARAM_ERROR[1] + u': 请求参数[%s]不合法' % each['name']
                                return response400({"c": REQUEST_PARAM_ERROR[0], "m": msg})
                            para_dict[key] = convertted
                    else:
                        para_dict[each['name']] = raw_para
                return func(request, para_dict, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)

        return returned_wrapper

    return decorator

