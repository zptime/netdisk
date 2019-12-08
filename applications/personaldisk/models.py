# -*- coding=utf-8 -*-
from django.db import models

from applications.upload_resumable.models import FileObj
from applications.user_center.models import Account
from utils.const_def import FALSE_INT, TRUE_INT


class NetdiskPersonalFile(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'用户', on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(u'名称', max_length=600)
    is_dir = models.PositiveSmallIntegerField(u'是否目录', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    fileobj = models.ForeignKey(FileObj, verbose_name=u'文件', on_delete=models.PROTECT, blank=True, null=True, related_name='personfileobj')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=u"上级目录")
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    class Meta:
        db_table = 'netdisk_personal_file'
        verbose_name_plural = u'个人网盘文件'
        verbose_name = u'个人网盘文件'

    def __unicode__(self):
        return '%s:%s' % (self.account.username, self.name)


class NetdiskPersonalSize(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'用户', on_delete=models.PROTECT, blank=True, null=True)
    totalsize = models.BigIntegerField(u'名称', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    class Meta:
        db_table = 'netdisk_personal_size'
        verbose_name_plural = u'个人网盘空间占用'
        verbose_name = u'个人网盘空间占用'

    def __unicode__(self):
        return '%s:%s' % (self.account.username, self.totalsize)

