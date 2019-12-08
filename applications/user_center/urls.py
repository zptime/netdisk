# -*- coding=utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    # 其它
    url(r'^api/login$', api_login),
    url(r'^api/logout$', api_logout),
    url(r'^api/refresh/item$', api_refresh_item),


    # 公共头部使用
    url(r'^api/list/service_apps$', api_list_service_apps),
    url(r'^api/detail/account$', api_detail_account),
    url(r'^api/reset/password$', api_reset_password),
    url(r'^api/list/user_type$', api_list_user_type),
    url(r'^api/change/user_type$', api_change_user_type),
    url(r'^api/get/user_center_url$', api_get_user_center_url),


    url(r'^api/upload/image$', api_upload_image),
    url(r'^api/update/teacher$', api_update_teacher),
    url(r'^api/update/parent$', api_update_parent),
    url(r'^api/update/student$', api_update_student),
    url(r'^api/list/grade$', api_list_grade),
    url(r'^api/list/class$', api_list_class),
    url(r'^api/school_list/subject$', api_school_list_subject),
    url(r'^api/school_list/textbook$', api_school_list_textbook),
    url(r'^api/list/teacher_textbook$', api_list_teacher_textbook),
    url(r'^api/update/teacher_textbook$', api_update_teacher_textbook),
    url(r'^api/add/teacher_textbook$', api_add_teacher_textbook),
    url(r'^api/delete/teacher_textbook$', api_delete_teacher_textbook),
    url(r'^api/list/teacher_class$', api_list_teacher_class),
    url(r'^api/delete/teacher_class$', api_delete_teacher_class),
    url(r'^api/add/teacher_class$', api_add_teacher_class),

    # 云盘程序内部使用
    url(r"^api/list/teacher_textbook_local$", api_list_teacher_textbook),  # 考虑到延时问题修改为从用户中心查询
    url(r"^api/list/school_textbook$", api_list_school_textbook),
    url(r"^api/list/chapter$", api_list_chapter),
    url(r"^api/list/school_subject$", api_list_subject),
    url(r"^api/list/title$", api_list_title),

]