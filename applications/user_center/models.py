# -*- coding=utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


SCHOOL_YEARS_ZERO = (0, u"未设置")
SCHOOL_YEARS_THREE = (3, u"三年制")
SCHOOL_YEARS_FOUR = (4, u"四年制")
SCHOOL_YEARS_FIVE = (5, u"五年制")
SCHOOL_YEARS_SIX = (6, u"六年制")
SCHOOL_YEARS_CHOICE = (SCHOOL_YEARS_ZERO, SCHOOL_YEARS_THREE, SCHOOL_YEARS_FOUR, SCHOOL_YEARS_FIVE, SCHOOL_YEARS_SIX)

SCHOOL_PERIOD_PRIMARY = (1, u"小学")
SCHOOL_PERIOD_JUNIOR = (2, u"初中")
SCHOOL_PERIOD_SENIOR = (4, u"高中")
SCHOOL_PERIOD_CHOICE = (SCHOOL_PERIOD_PRIMARY, SCHOOL_PERIOD_JUNIOR, SCHOOL_PERIOD_SENIOR)


class School(models.Model):
    code = models.CharField(max_length=30, verbose_name=u'学校标识码')
    name_simple = models.CharField(default="", blank=True, max_length=30, verbose_name=u'学校简称')
    name_full = models.CharField(max_length=30, verbose_name=u'学校全称')
    name_english = models.CharField(default="", blank=True, max_length=30, verbose_name=u'学校英文名称')

    property = models.CharField(default="", blank=True, choices=((u"公办", u"公办"), (u"民办", u"民办")), max_length=30,
                                verbose_name=u'学校属性')
    nature = models.CharField(default="", blank=True, choices=((u"部属", u"部属"), (u"省属", u"省属"), (u"市属", u"市属"),
                                                   (u"区属", u"区属")), max_length=30, verbose_name=u'学校性质')
    type = models.CharField(default="", blank=True, choices=((u"小学", u"小学"), (u"初级中学", u"初级中学"), (u"九年一贯制", u"九年一贯制"),
                                                 (u"高级中学", u"高级中学")), max_length=30, verbose_name=u'办学类别')
    primary_years = models.IntegerField(default=0, choices=((0, u"未设置"), (5, u"小学五年制"), (6, u"小学六年制")), verbose_name=u'小学年制')
    junior_years = models.IntegerField(default=0, choices=((0, u"未设置"), (3, u"初中三年制"), (4, u"初中四年制")), verbose_name=u'初中年制')
    senior_years = models.IntegerField(default=0, choices=((0, u"未设置"), (3, u"高中三年制")),verbose_name=u'高中年制')
    academic_year = models.IntegerField(default=6, choices=((3, u"三年制"), (4, u"四年制"), (5, u"五年制"),
                                                            (6, u"六年制"), (9, u"九年制"), (12, u"十二年制")), verbose_name=u"学制年限")
    province = models.CharField(default="", blank=True, max_length=30, verbose_name=u'省')
    city = models.CharField(default="", blank=True, max_length=30, verbose_name=u'市')
    district = models.CharField(default="", blank=True, max_length=30, verbose_name=u'区/县')
    town = models.CharField(default="", blank=True, max_length=30, verbose_name=u'镇/乡')
    village = models.CharField(default="", blank=True, max_length=30, verbose_name=u'村')
    street = models.CharField(default="", blank=True, max_length=30, verbose_name=u'街道')
    doorplate = models.CharField(default="", blank=True, max_length=30, verbose_name=u'门牌')

    superior_org = models.CharField(default="", blank=True, max_length=30, verbose_name=u'直属主管机构')
    founding_year = models.CharField(default="", blank=True, max_length=30, verbose_name=u'建校年月')
    anniversary = models.CharField(default="", blank=True, max_length=30, verbose_name=u'校庆日')

    phone = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系电话')
    fox = models.CharField(default="", blank=True, max_length=30, verbose_name=u'传真电话')
    zip = models.CharField(default="", blank=True, max_length=30, verbose_name=u'建校年月')
    web_site = models.CharField(default="", blank=True, max_length=30, verbose_name=u'建校年月')

    contact_person = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系人姓名')
    contact_mobile = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系人移动电话')
    contact_title = models.CharField(default="", blank=True, max_length=30, verbose_name=u'联系人职务')
    intro = models.CharField(default="", blank=True, max_length=512, verbose_name=u'学校简介')

    footer = models.CharField(default="", blank=True, max_length=256, verbose_name=u"主页底部显示内容")
    logo_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u"学校logo图")
    title = models.CharField(default="", blank=True, max_length=32, verbose_name=u"学校title显示")

    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否激活')
    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_school"
        verbose_name_plural = u"学校"
        verbose_name = u"学校"

    def __unicode__(self):
        return self.name_full


class Title(models.Model):
    school = models.ForeignKey(School, verbose_name=u"所属学校", related_name="title_school_related", on_delete=models.PROTECT)
    name = models.CharField(default='', max_length=30, verbose_name=u'职务名称')
    type = models.IntegerField(default=2, choices=((1, u"系统内置"), (2, u"用户自定义")), verbose_name=u'职务类型')
    comments = models.CharField(default='', max_length=256, verbose_name=u'职务名称')
    teacher_amount = models.IntegerField(default=0, blank=True, verbose_name=u'教师人数')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'uc_title'
        verbose_name = u'职务'
        verbose_name_plural = u'职务'

    def __unicode__(self):
        return self.name


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if (not username) or (not password):
            raise ValueError('UserManager create user param error')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        if kwargs:
            if kwargs.get('email', ""):
                user.email = kwargs['email']
            elif kwargs.get('full_name', ""):
                user.full_name = kwargs['full_name']
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        account = self.create_user(username=username, password=password)
        account.is_superuser = True
        account.is_admin = True
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, db_index=True, verbose_name=u'账号')
    code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'学籍号')  # 学生
    mobile = models.CharField(default="", max_length=30, blank=True, null=True, verbose_name=u'手机号')  # 学生、教师、家长
    parent_mobile = models.CharField(default="", max_length=30, blank=True, null=True, verbose_name=u'家长手机号') # 学生

    type = models.IntegerField(default=0, choices=((0, u"未设置"), (1, u"学生"), (2, u"教师"), (4, u"家长")), verbose_name=u'用户类型')
    school = models.ForeignKey(School, blank=True, null=True, verbose_name=u'当前所在学校', on_delete=models.PROTECT)
    role = models.CharField(default="", max_length=254, blank=True, verbose_name=u'角色')

    is_admin = models.BooleanField(default=False, verbose_name=u'是否后台管理员')
    is_active = models.BooleanField(default=True, verbose_name=u'有效')
    encoded_pwd = models.CharField(max_length=128, verbose_name=u'加密密码')

    need_change_pwd = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否需要修改密码')
    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')


    # 暂时不使用
    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    tmp_code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'学籍号（L）/员工号')
    full_name = models.CharField(max_length=30, blank=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", blank=True, max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"),
                                                                   (u"女", u"女")), verbose_name=u'性别')
    email = models.CharField(default="", max_length=254, blank=True,  verbose_name=u'邮箱')
    is_mobile_login = models.IntegerField(default=0, blank=True, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否允许手机登录')
    is_email_login = models.IntegerField(default=0, blank=True, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否允许邮箱登陆')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    company = models.CharField(default="", blank=True,  max_length=30, verbose_name=u'单位')
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.full_name

    class Meta:
        db_table = "uc_account"
        verbose_name_plural = u"用户表"
        verbose_name = u"用户表"

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Grade(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    grade_num = models.IntegerField(verbose_name=u'年级序号')
    grade_name = models.CharField(default="", max_length=30, verbose_name=u'年级名称')

    class_amount = models.IntegerField(default=0,  blank=True, verbose_name=u'年级班级总数')
    period_grade_num = models.IntegerField(verbose_name=u'学段内年级序号')
    school_period = models.IntegerField(default=0,  blank=True, choices=SCHOOL_PERIOD_CHOICE, verbose_name=u'学段')
    school_years = models.IntegerField(default=0, blank=True, choices=SCHOOL_YEARS_CHOICE, verbose_name=u'年制')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_grade"
        verbose_name_plural = u"年级"
        verbose_name = u"年级"

    def __unicode__(self):
        return self.grade_name


class Class(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    # teacher = models.ForeignKey(Teacher, verbose_name=u'班主任')
    grade_num = models.IntegerField(default=0, null=True, verbose_name=u"年级编号")  # （1~12）
    period_grade_num = models.IntegerField(default=0, verbose_name=u'学段内年级序号')
    class_num = models.IntegerField(verbose_name=u'班级编号')
    class_name = models.CharField(default="", blank=True, max_length=30, verbose_name=u'班级名称')
    grade_name = models.CharField(default="", blank=True, max_length=30, verbose_name=u'年级名称')
    enrollment_year = models.IntegerField(default=0, verbose_name=u'入学年度')
    graduate_year = models.IntegerField(default=0, blank=True, verbose_name=u'毕业年度')
    graduate_status = models.IntegerField(default=0, choices=((1, u"是"),(0, u"否")), verbose_name=u'是否毕业')

    student_amount = models.IntegerField(default=0,  blank=True, verbose_name=u'班级学生总数')
    class_alias = models.CharField(default="", blank=True, max_length=30, verbose_name=u'班级别名')
    school_period = models.IntegerField(default=0,  blank=True, choices=SCHOOL_PERIOD_CHOICE, verbose_name=u'学段')
    school_years = models.IntegerField(default=0, blank=True, choices=SCHOOL_YEARS_CHOICE, verbose_name=u'年制')
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_class"
        verbose_name_plural = u"班级"
        verbose_name = u"班级"

    def __unicode__(self):
        return self.class_name


class Teacher(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'账号', on_delete=models.PROTECT)

    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    email = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'邮箱')
    full_name = models.CharField(max_length=30, db_index=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"), (u"女", u"女")), verbose_name=u'性别')
    school_code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u"教工号")
    tmp_code = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u"临时教工号")

    birthday = models.DateTimeField(blank=True, null=True, verbose_name=u'生日')
    native_place = models.CharField(default="", blank=True, max_length=30, verbose_name=u'籍贯')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')
    banner_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'主页图片')

    cls = models.ForeignKey(Class, blank=True, null=True,  verbose_name=u'管理班级', on_delete=models.PROTECT)
    title = models.ForeignKey(Title, blank=True, null=True,  verbose_name=u'职务', on_delete=models.PROTECT)
    kind = models.CharField(default="", blank=True, max_length=30, verbose_name=u'类型')
    is_in = models.BooleanField(default=True, verbose_name=u'是否在校')
    is_available = models.BooleanField(default=True, verbose_name=u'是否有效')

    in_date = models.DateTimeField(blank=True, null=True, verbose_name=u'入校时间')
    out_date = models.DateTimeField(blank=True, null=True, verbose_name=u'出校时间')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_teacher"
        verbose_name_plural = u"教师"
        verbose_name = u"教师"

    def __unicode__(self):
        return self.full_name


class Student(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'账号', on_delete=models.PROTECT)

    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    email = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'邮箱')
    full_name = models.CharField(max_length=30, db_index=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"), (u"女", u"女")), verbose_name=u'性别')

    birthday = models.DateTimeField(blank=True, null=True, verbose_name=u'生日')
    native_place = models.CharField(default="", max_length=30, verbose_name=u'籍贯')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')
    banner_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'主页图片')

    cls = models.ForeignKey(Class, null=True, blank=True, verbose_name=u'班级', on_delete=models.PROTECT)
    kind = models.CharField(default="", blank=True, max_length=30, verbose_name=u'学生类型')
    is_in = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否在读')
    is_available = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否有效')

    entry_date = models.DateTimeField(blank=True, null=True, verbose_name=u'入校时间')
    out_date = models.DateTimeField(blank=True, null=True, verbose_name=u'出校时间')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_student"
        verbose_name_plural = u"学生"
        verbose_name = u"学生"

    def __unicode__(self):
        return self.full_name


class Parent(models.Model):
    school = models.ForeignKey(School, verbose_name=u'所属学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'账号', related_name="parent_account", on_delete=models.PROTECT)

    id_card = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'身份证号')
    email = models.CharField(default="", max_length=254, blank=True, null=True, verbose_name=u'邮箱')
    full_name = models.CharField(max_length=30, db_index=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"), (u"女", u"女")), verbose_name=u'性别')

    birthday = models.DateTimeField(blank=True, null=True, verbose_name=u'生日')
    native_place = models.CharField(default="", max_length=30, verbose_name=u'籍贯')
    address = models.CharField(default="", blank=True, max_length=128, verbose_name=u'地址')
    company = models.CharField(default="", blank=True,  max_length=30, verbose_name=u'单位')
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')
    banner_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'主页图片')

    comments = models.CharField(default="",  blank=True, max_length=512, verbose_name=u'备注')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否激活')


    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_parent"
        verbose_name_plural = u"家长"
        verbose_name = u"家长"

    def __unicode__(self):
        return self.full_name


# 申请状态
APPLICATION_STATUS_NOT_PROCESS = (1, u"未处理")
APPLICATION_STATUS_APPROVED = (2, u"已同意")
APPLICATION_STATUS_REFUSED = (3, u"已拒绝")
APPLICATION_STATUS_CHOICE = (APPLICATION_STATUS_NOT_PROCESS, APPLICATION_STATUS_APPROVED, APPLICATION_STATUS_REFUSED)


class ParentStudent(models.Model):
    parent = models.ForeignKey(Parent, verbose_name=u'家长', on_delete=models.PROTECT)
    student = models.ForeignKey(Student, verbose_name=u'孩子', related_name="child_account", on_delete=models.PROTECT)
    relation = models.CharField(default="",  blank=True, max_length=30, verbose_name=u'所属关系')
    comments = models.CharField(default="",  blank=True, max_length=512, verbose_name=u'备注')
    status = models.IntegerField(default=APPLICATION_STATUS_APPROVED[0], choices=APPLICATION_STATUS_CHOICE, verbose_name=u'处理状态')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_parent_student"
        verbose_name_plural = u"家长学生"
        verbose_name = u"家长学生"

    def __unicode__(self):
        return str(self.id)

SERVICE_ACCESS_MASK_CHOICE = ((1, u"学生"), (2, u"教师"), (3, u"学生|教师"), (4, u"家长"), (5, u"学生|家长"),
                              (6, u"教师|家长"), (7, u"学生|教师|家长"), (0, u"只对管理员开放"),)

SERVICE_CLASSIFY_CHOICE = ((1, u"基础服务"), (2, u"拓展服务"))


class Service(models.Model):
    code = models.CharField(max_length=30, verbose_name=u'服务编码')
    name = models.CharField(max_length=30, verbose_name=u'服务名称')
    type = models.IntegerField(default=0, choices=((1, u"内部服务"), (2, u"第三方服务")), verbose_name=u'服务类型')
    intranet_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'内网服务访问地址')
    internet_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'外网服务访问地址')
    access_key = models.CharField(default="", blank=True, max_length=30, verbose_name=u'服务访问ID')
    secret_key = models.CharField(default="", blank=True, max_length=30, verbose_name=u'服务访问密钥')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')

    access_mask = models.IntegerField(default=7, choices=SERVICE_ACCESS_MASK_CHOICE, verbose_name=u"允许访问的用户类型")
    is_cls_adviser_as_mgr = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'班主任是否视为管理员')

    classify = models.IntegerField(default=0, choices=SERVICE_CLASSIFY_CHOICE, verbose_name=u"服务归类管理")

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_service"
        verbose_name_plural = u"服务"
        verbose_name = u"服务"

    def __unicode__(self):
        return self.name


class Role(models.Model):
    service = models.ForeignKey(Service, verbose_name=u'所属服务', on_delete=models.PROTECT)
    code = models.CharField(default="", max_length=30, verbose_name=u'角色编号')
    name = models.CharField(default="", max_length=30, verbose_name=u'角色名称')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_role"
        verbose_name_plural = u"角色"
        verbose_name = u"角色"

    def __unicode__(self):
        return self.name


class UserRole(models.Model):
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)
    role = models.ForeignKey(Role, verbose_name=u'用户角色', on_delete=models.PROTECT)
    user = models.ForeignKey(Teacher, verbose_name=u'用户', on_delete=models.PROTECT)

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_user_role"
        verbose_name_plural = u"用户角色"
        verbose_name = u"用户角色"

    def __unicode__(self):
        return str(self.id)


class Subnet(models.Model):
    cidr = models.CharField(max_length=30, verbose_name=u'子网描述字符串CIDR')
    comments = models.CharField(default="", blank=True, max_length=512, verbose_name=u'备注')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_subnet"
        verbose_name_plural = u"内网子网"
        verbose_name = u"内网子网"

    def __unicode__(self):
        return self.cidr


class Subject(models.Model):
    name = models.CharField(default="", max_length=30, blank=True, db_index=True, verbose_name=u'名称')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否生效')
    editor = models.ForeignKey(Account, blank=True, null=True, verbose_name=u'编辑者', on_delete=models.PROTECT)
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_subject"
        verbose_name_plural = u"科目"
        verbose_name = u"科目"

    def __unicode__(self):
        return self.name


# 年级
GRADE_NUM_NOT_SET = (0, u"未设置")
GRADE_NUM_FIRST = (1, u"一年级")
GRADE_NUM_SECOND = (2, u"二年级")
GRADE_NUM_THIRD = (3, u"三年级")
GRADE_NUM_FOURTH = (4, u"四年级")
GRADE_NUM_FIFTH = (5, u"五年级")
GRADE_NUM_SIXTH = (6, u"六年级")
GRADE_NUM_SEVENTH = (7, u"七年级")
GRADE_NUM_EIGHTH = (8, u"八年级")
GRADE_NUM_NINTH = (9, u"九年级")
GRADE_NUM_TENTH = (10, u"高一")
GRADE_NUM_ELEVENTH = (11, u"高二")
GRADE_NUM_TWELFTH = (12, u"高三")

GRADE_NUM_CHOICE = (GRADE_NUM_FIRST, GRADE_NUM_SECOND, GRADE_NUM_THIRD, GRADE_NUM_FOURTH, GRADE_NUM_FIFTH,
                      GRADE_NUM_SIXTH, GRADE_NUM_SEVENTH, GRADE_NUM_EIGHTH, GRADE_NUM_NINTH, GRADE_NUM_TENTH,
                      GRADE_NUM_ELEVENTH, GRADE_NUM_TWELFTH)


class Textbook(models.Model):
    name = models.CharField(default="", max_length=128, blank=True, db_index=True, verbose_name=u'名称')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否生效')
    editor = models.ForeignKey(Account, blank=True, null=True, verbose_name=u'编辑者', on_delete=models.PROTECT)
    image_url = models.CharField(default="", max_length=256, blank=True, verbose_name=u'图片')
    subject = models.ForeignKey(Subject, verbose_name=u'科目', on_delete=models.PROTECT)
    grade_num = models.IntegerField(default=GRADE_NUM_NOT_SET[0], choices=GRADE_NUM_CHOICE, verbose_name=u'年级编号')
    chapter_count = models.IntegerField(default=0, verbose_name=u'章节数目')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_textbook"
        verbose_name_plural = u"教材"
        verbose_name = u"教材"

    def __unicode__(self):
        return self.name


class Chapter(models.Model):
    textbook = models.ForeignKey(Textbook, verbose_name=u'教材', on_delete=models.PROTECT)
    name = models.CharField(default="", max_length=128, blank=True, db_index=True, verbose_name=u'名称')
    parent_id = models.IntegerField(default=None, null=True, blank=True, verbose_name=u'父节点ID')
    open = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否展开')
    is_parent = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为没有子节点的父节点')
    sn = models.IntegerField(null=True, blank=True, verbose_name=u'编号')
    # 备用字段
    up_brother = models.ForeignKey('self', null=True, blank=True, verbose_name=u'上一个的兄弟节点的ID', on_delete=models.PROTECT, related_name="up_brother_related")
    resource_count = models.IntegerField(default=0, verbose_name=u'资源数量')
    is_active = models.IntegerField(default=1, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否生效')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_chapter"
        verbose_name_plural = u"章节"
        verbose_name = u"章节"

    def __unicode__(self):
        return self.name


class SchoolSubject(models.Model):
    subject = models.ForeignKey(Subject, verbose_name=u'科目', on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_school_subject"
        verbose_name_plural = u"学校开设科目"
        verbose_name = u"学校开设科目"

    def __unicode__(self):
        return str(self.id)


class SchoolTextbook(models.Model):
    textbook = models.ForeignKey(Textbook, verbose_name=u'教材', on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name=u'学校', on_delete=models.PROTECT)

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_school_textbook"
        verbose_name_plural = u"学校使用教材"
        verbose_name = u"学校使用教材"

    def __unicode__(self):
        return str(self.id)


class TeacherClass(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师', on_delete=models.PROTECT)
    cls = models.ForeignKey(Class, verbose_name=u'班级', on_delete=models.PROTECT)
    is_master = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为班主任')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_teacher_class"
        verbose_name_plural = u"教师所授班级"
        verbose_name = u"教师所授班级"

    def __unicode__(self):
        return str(self.id)


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师', related_name="teacher_subject_teacher_related",  on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, verbose_name=u'所授科目', related_name="teacher_subject_subject_related", on_delete=models.PROTECT)
    is_current = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为当前科目')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_teacher_subject"
        verbose_name_plural = u"教师所授科目"
        verbose_name = u"教师所授科目"

    def __unicode__(self):
        return str(self.id)


class TeacherTextbook(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师',  related_name="teacher_textbook_teacher_related", on_delete=models.PROTECT)
    textbook = models.ForeignKey(Textbook, verbose_name=u'所授教材', related_name="teacher_textbook_textbook_related", on_delete=models.PROTECT)
    is_current = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否为当前教材')

    create_time = models.DateTimeField(verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_teacher_textbook"
        verbose_name_plural = u"教师使用教材"
        verbose_name = u"教师使用教材"

    def __unicode__(self):
        return str(self.id)


class SchoolService(models.Model):
    service = models.ForeignKey(Service, verbose_name=u'服务')
    school = models.ForeignKey(School, verbose_name=u'学校')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = "uc_school_service"
        verbose_name_plural = u"学校服务"
        verbose_name = u"学校服务"

    def __unicode__(self):
        return str(self.id)
