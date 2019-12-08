# -*- coding=utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView

from applications.common.views import *


urlpatterns = [
    url(r'^logout', RedirectView.as_view(url='html/logout', permanent=False)),
    url(r'^api/common/logout', api_logout),
    url(r'^api/mobile/heartbeat', api_mobile_heartbeat),

    url(r'^api/common/setting/detail', api_common_setting_detail),

    url(r'^api/common/class/list', api_common_class_list),    # 返回在校的年级和班级（不包含已毕业的班）
    url(r'^api/common/title/list', api_common_title_list),
    url(r'^api/common/teacher/list', api_common_teacher_list),
    url(r'^api/common/student/list', api_common_student_list),

]
