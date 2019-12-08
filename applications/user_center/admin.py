#!/usr/bin/env python
# coding=utf-8
from django.contrib import admin
from models import *


class AccountAppAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'type', 'school']
    exclude = ('status', 'num', 'encoded_pwd', 'is_admin', 'last_login', 'create_time', 'update_time', 'del_flag')

admin.site.register(Account, AccountAppAdmin)


class SchoolAppAdmin(admin.ModelAdmin):
    list_display = ['name_full',  'code', 'property', 'intro', 'del_flag']
    list_filter = ['name_full', 'del_flag']

admin.site.register(School, SchoolAppAdmin)


class GradeAppAdmin(admin.ModelAdmin):
    list_display = ['school',  'grade_num', 'grade_name', 'del_flag']
    list_filter = ['grade_num', 'del_flag']

admin.site.register(Grade, GradeAppAdmin)


class ClassAppAdmin(admin.ModelAdmin):
    list_display = ['school',  'class_num', 'class_name', 'enrollment_year', 'del_flag']
    list_filter = ['class_name', 'del_flag']

admin.site.register(Class, ClassAppAdmin)


class StudentAppAdmin(admin.ModelAdmin):
    list_display = ['id',  'school', 'account', 'full_name', 'cls', 'is_in', 'is_available', 'del_flag']
    list_filter = ['account', 'del_flag']

admin.site.register(Student, StudentAppAdmin)
