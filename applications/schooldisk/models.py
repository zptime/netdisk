# -*- coding=utf-8 -*-
from django.db import models

from applications.upload_resumable.models import FileObj
from applications.user_center.models import Account, School, Teacher
from utils.const_def import *


class NetdiskSchoolFile(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT, blank=True, null=True)
    account = models.ForeignKey(Account, verbose_name=u'用户', on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(u'名称', max_length=600)
    is_dir = models.PositiveSmallIntegerField(u'是否目录', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    fileobj = models.ForeignKey(FileObj, verbose_name=u'文件', on_delete=models.PROTECT, blank=True, null=True, related_name='schoolfileobj')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u"上级目录")
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    class Meta:
        db_table = 'netdisk_school_file'
        verbose_name_plural = u'学校网盘文件'
        verbose_name = u'学校网盘文件'

    def __unicode__(self):
        return '%s %s:%s' % (self.school.name_full, self.account.username, self.name)


class NetdiskSchoolSize(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT, blank=True, null=True)
    totalsize = models.BigIntegerField(u'名称', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    class Meta:
        db_table = 'netdisk_school_size'
        verbose_name_plural = u'学校网盘空间占用'
        verbose_name = u'学校网盘空间占用'

    def __unicode__(self):
        return '%s:%s' % (self.school.name_full, self.totalsize)


class NetdiskSchoolRole(models.Model):
    netdiskschoolfile = models.ForeignKey(NetdiskSchoolFile, verbose_name=u'学校', on_delete=models.PROTECT, blank=True, null=True)
    account = models.ForeignKey(Account, verbose_name=u'用户', on_delete=models.PROTECT, blank=True, null=True)  # 用户为空时，代表所有人都有权限。
    teacher = models.ForeignKey(Teacher, verbose_name=u'老师', on_delete=models.PROTECT, blank=True, null=True)  # 用户为空时，代表所有人都有权限。
    role_type = models.PositiveSmallIntegerField(u'权限类型', default=ROLE_TYPE_NONE, choices=((ROLE_TYPE_NONE, u'无权限'), (ROLE_TYPE_ADMIN, u'管理员'), (ROLE_TYPE_LIST, u'查看'), (ROLE_TYPE_UPLOAD, u'上传'), (ROLE_TYPE_DOWNLOAD, u'下载')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    class Meta:
        db_table = 'netdisk_school_role'
        verbose_name_plural = u'学校网盘权限'
        verbose_name = u'学校网盘权限'

    def __unicode__(self):
        return '%s %s:%s' % (self.account.full_name, self.netdiskschoolfile.name, self.role_type)

