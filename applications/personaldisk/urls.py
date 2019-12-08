# -*- coding=utf-8 -*-

from django.conf.urls import url
from applications.personaldisk.views import *

urlpatterns = [
    url(r'^api/test$', api_test),
    url(r'^api/persondisk/summary$', api_persondisk_summary),
    url(r'^api/persondisk/adddir$', api_persondisk_adddir),
    url(r'^api/persondisk/modname$', api_persondisk_modname),
    url(r'^api/persondisk/filelist$', api_persondisk_filelist),
    url(r'^api/persondisk/submitfile$', api_persondisk_submitfile),
    url(r'^api/persondisk/delfile$', api_persondisk_delfile),
    url(r'^api/persondisk/movfile$', api_persondisk_movfile),
    url(r'^api/persondisk/refreshspace$', api_persondisk_refreshspace),
    url(r'^api/persondisk/getdownloadurl$', api_persondisk_getdownloadurl),
    url(r'^api/persondisk/checkauth/(?P<file_name>.*)$', api_persondisk_checkauth),
]
