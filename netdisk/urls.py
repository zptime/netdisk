# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from templates.html import home_page


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='html/%s' % home_page, permanent=False)),
    url(r'^user_center/', include('applications.user_center.urls')),
    url(r'', include('applications.common.urls')),

    # 补充各个application的自定义url
    url(r'', include('applications.personaldisk.urls')),
    url(r'', include('applications.upload_resumable.urls')),
    url(r'', include('applications.schooldisk.urls')),
]

# swagger
urlpatterns += patterns('applications.swagger.views',
    url(r'^api/$', 'api_index'),
    url(r'^api/docs/$', 'api_docs'),
)

# html page
urlpatterns += patterns('templates.html',
    url(r'^html/(?P<raw_path>.*)$', 'html_handler'),
    url(r'^m/', 'page_mobile'),
)

# page's favicon
urlpatterns += patterns('', (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),)

urlpatterns += staticfiles_urlpatterns()   # static

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': os.path.join(settings.BASE_DIR, 'media'),}),
    )
