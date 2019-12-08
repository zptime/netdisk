# -*- coding=utf-8 -*-
from django.conf import settings
from django.db import models

from applications.user_center.models import *
from utils.const_def import *


class Setting(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT, blank=True, null=True)
    key = models.CharField(u'键', max_length=100)
    value = models.CharField(u'值', max_length=5000, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    class Meta:
        db_table = 'common_setting'
        verbose_name_plural = u'参数定义表'
        verbose_name = u'参数定义表'

    def __unicode__(self):
        return 'Setting(%s %s:%s)' % (self.school.name_full, self.key, self.value)


