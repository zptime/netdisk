# -*- coding=utf-8 -*-

from django.conf.urls import url
from applications.schooldisk.views import *

urlpatterns = [
    url(r'^api/schooldisk/summary$', api_schooldisk_summary),
    url(r'^api/schooldisk/adddir$', api_schooldisk_adddir),
    url(r'^api/schooldisk/moddir$', api_schooldisk_moddir),
    url(r'^api/schooldisk/qrydir$', api_schooldisk_qrydir),
    url(r'^api/schooldisk/filelist$', api_schooldisk_filelist),
    url(r'^api/schooldisk/submitfile$', api_schooldisk_submitfile),
    url(r'^api/schooldisk/delfile$', api_schooldisk_delfile),
    url(r'^api/schooldisk/movfile$', api_schooldisk_movfile),
    url(r'^api/schooldisk/refreshspace$', api_schooldisk_refreshspace),
    url(r'^api/schooldisk/getdownloadurl$', api_schooldisk_getdownloadurl),
    url(r'^api/schooldisk/getoatarget$', api_schooldisk_getoatarget),
    url(r'^api/schooldisk/getuserdirrole$', api_schooldisk_getuserdirrole),
    url(r'^api/schooldisk/getuserfilerole$', api_schooldisk_getuserfilerole),
    url(r'^api/schooldisk/dirstatistics$', api_schooldisk_dirstatistics),
    url(r'^api/schooldisk/dayuploadinfo$', api_schooldisk_dayuploadinfo),
    url(r'^api/schooldisk/alldirsummary$', api_schooldisk_alldirsummary),
]
