# -*- coding: utf-8 -*-

import datetime
import types
import logging

from django.conf import settings
from django.contrib.auth import logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, resolve_url, render_to_response
from django_cas_ng import views as cas_views

from applications.schooldisk.service import api_schooldisk_getuserdirrole
from utils.check_obj import check_get_teacher_by_request
from utils.const_err import *
from utils.net_helper import *
from utils.utils_type import bool2str

from applications.user_center.models import Service, UserRole, Role

logger = logging.getLogger(__name__)


@login_required
def page_mobile(request):
    return render(request, 'mobile/index.html')


def html_handler(request, raw_path):
    path = raw_path.rstrip('/')
    if path not in url_mapping:
        raise Http404
    handler = url_mapping[path]
    for each_auth in handler['functions_auth']:
        if isinstance(each_auth, types.FunctionType):
            is_auth, to_where = each_auth(request)
            if not is_auth:
                return redirect_mapping[to_where](request)
    customized_handler = handler['function_customize']
    if customized_handler:
        return customized_handler(request)
    else:
        ctx_function = handler['function_ctx']
        html_goto = handler['html_goto']
        ctx = dict()
        if isinstance(ctx_function, types.FunctionType):
            ctx = ctx_function(request)
        return render(request, html_goto, ctx)


def _goto_page_login(request):
    return redirect_login_page(request)


def _goto_page_noauth(request):
    return render(request, 'html/noauth.html')


def cas_logout(request):
    return cas_views.logout(request)


def cas_login(request):
    return cas_views.login(request)


def redirect_login_page(request):
    path = request.build_absolute_uri()
    resolved_login_url = resolve_url(settings.LOGIN_URL)
    login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    current_scheme, current_netloc = urlparse(path)[:2]
    if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
        path = request.get_full_path()
    from django.contrib.auth.views import redirect_to_login
    return redirect_to_login(
        path, resolved_login_url, REDIRECT_FIELD_NAME)


def auth_is_login(request):
    """
        登录才能访问本页
    """
    if request.user.username == settings.DB_ADMIN:
        return False, TO_NOAUTH
    if not request.user.is_authenticated():
        return False, TO_LOGIN
    return True, None


def auth_is_teacher(request):
    """
        教师才能访问本页
    """
    is_auth, to_where = auth_is_login(request)
    if not is_auth:
        return False, to_where
    is_teacher = request.user.type == USER_TYPE_TEACHER
    return is_teacher, TO_NOAUTH


def auth_is_sysadmin(request):
    """
        用户中心定义的系统管理员才能访问本页
    """
    is_auth, to_where = auth_is_teacher(request)
    if not is_auth:
        return False, to_where
    teacher = check_get_teacher_by_request(request)
    current_services = Service.objects.filter(code__in=settings.SYSTEM_SERVICES, del_flag=FALSE_INT)
    super_role = Role.objects.filter(service__in=current_services, code=SUPER_ADMIN_CODE, del_flag=FALSE_INT).first()
    is_sysadmin = UserRole.objects.filter(user=teacher, school=teacher.school, role=super_role, del_flag=FALSE_INT).exists()
    return is_sysadmin, TO_NOAUTH


def ctx_is_sysadmin(request):
    is_sysadmin, TO_NOAUTH = auth_is_sysadmin(request)
    return {'is_sysadmin' : bool2str(is_sysadmin)}


def html_upload_file(request):
    dir_file_id = request.GET.get('dir_file_id')
    userdirrole = api_schooldisk_getuserdirrole(request.user, dir_file_id)
    if ROLE_TYPE_ADMIN in userdirrole:
        return render(request, 'page/管理员页面.html')
    elif ROLE_TYPE_LIST in userdirrole:
        return render(request, 'html/列表权限.html')
    elif ROLE_TYPE_UPLOAD in userdirrole:
        return render(request, 'html/上传权限.html')
    elif ROLE_TYPE_DOWNLOAD in userdirrole:
        return render(request, 'html/下载权限.html')

    return render(request, 'mobile/无权限.html')


TO_LOGIN = 'TO_LOGIN'
TO_NOAUTH = 'TO_NOAUTH'
redirect_mapping = {
    TO_LOGIN: _goto_page_login,
    TO_NOAUTH: _goto_page_noauth,
}


home_page='index'

url_mapping = {
    'login': {
        # 认证函数链，任意一个不通过则跳转noauth.html
        'functions_auth': (),
        # 上下文生成函数
        'function_ctx': None,
        # 最后的跳转页
        'html_goto': '',
        # 自定义处理 (将无视'html_goto'和'function_ctx'配置)
        'function_customize': cas_login,
    },

    'logout': {
        'functions_auth': (),
        'function_ctx': None,
        'html_goto': '',
        'function_customize': cas_logout,
    },
    'locallogin': {
        'functions_auth': (),
        'function_ctx': None,
        'html_goto': 'common/login.html',
        'function_customize': None,
    },

    'index': {
        'functions_auth': (),
        'function_ctx': ctx_is_sysadmin,
        'html_goto': 'page/index.html',
        'function_customize': None,
    },
    'root': {
        'functions_auth': (),
        'function_ctx': ctx_is_sysadmin,
        'html_goto': 'page/root.html',
        'function_customize': None,
    },
    'document/statistics': {
        'functions_auth': (),
        'function_ctx': ctx_is_sysadmin,
        'html_goto': 'page/teacher/statistics.html',
        'function_customize': None,
    },
    'upload/file': {
        'functions_auth': (auth_is_login,),
        'function_ctx': None,
        'html_goto': '',
        'function_customize': html_upload_file,
    },
    'personalDisk': {
        'functions_auth': (),
        'function_ctx': ctx_is_sysadmin,
        'html_goto': 'page/personal/personalDisk.html',
        'function_customize': None,
    },
}
