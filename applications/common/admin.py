# -*- coding: utf-8 -*-

from django.contrib import admin

from applications.common.models import *


class SettingAdmin(admin.ModelAdmin):
    list_display = ['school', 'key', 'value', 'is_del']
    readonly_fields = ['id', 'create_time', 'update_time']
    list_filter = ['school']

admin.site.register(Setting, SettingAdmin)






