# -*- coding=utf-8 -*-
from models import *
from utils import *
from django.conf import settings
from django.contrib import auth


def get_user_obj(account):
    if account.type == USER_TYPE_STUDENT:
        return Student.objects.filter(school_id=account.school_id, account_id=account.id, del_flag=FLAG_NO).first()
    elif account.type == USER_TYPE_TEACHER:
        return Teacher.objects.filter(school_id=account.school_id, account_id=account.id, del_flag=FLAG_NO).first()
    elif account.type == USER_TYPE_PARENT:
        return Parent.objects.filter(school_id=account.school_id, account_id=account.id, del_flag=FLAG_NO).first()
    else:
        return None


def get_user_type(teacher_obj, service_code):
    user_role = UserRole.objects.filter(user=teacher_obj, role__service__code=service_code, del_flag=FLAG_NO).\
        values_list("role__code", flat=True)
    if user_role:
        return user_role[0]
    else:
        return None


def get_image_url(image_name):
    if not image_name:
        return ""
    path = '/' + settings.SERVICE_USER_CENTER_BUCKET + '/' + image_name
    if settings.USER_CENTER_S3_HOST:
        image_url = 'http://' + settings.USER_CENTER_S3_HOST + path
    else:
        image_url = get_user_center_url() + path
    return image_url


def login(request, username, password):
    user = Account.objects.filter(username=username).first()
    if not user:
        user = Account.objects.filter(mobile=username).first()
    if not user:
        user = Account.objects.filter(code=username).first()
    if user:
        user = auth.authenticate(username=user.username, password=password)
    else:
        user = None
    if user is not None and user.is_active:
        auth.login(request, user)
        return True
    return False


def call_api(request, api_name):
    user_id = request.user.id
    parameters = {}
    for key, value in request.POST.items():
        parameters[key] = value
    # url = settings.USER_CENTER_URL + settings.API_USER_CENTER_CALL_API
    domain_list = get_uc_internal_domain_list()
    form_data_dict = {"user_id": user_id, "api_name": api_name}
    if parameters:
        form_data_dict["parameters"] = json.dumps(parameters, ensure_ascii=False)
    file_data_dict = {}
    for filed_name, file in request.FILES.items():
        file_data_dict[filed_name] = (file.name, file.file)

    resp_data = try_send_http_request(domain_list=domain_list, path=settings.API_USER_CENTER_CALL_API,
                                      method="POST", form_data_dict=form_data_dict, file_data_dict=file_data_dict)
    return resp_data


def get_service_url(service_name, internet=True):
    user_center_obj = Service.objects.get(code=service_name, del_flag=FLAG_NO)
    if internet:
        url = get_domain_name(user_center_obj.internet_url)
    else:
        url = get_domain_name(user_center_obj.intranet_url)
    return url


def get_user_center_url():
    user_center_obj = Service.objects.get(code=settings.SERVICE_USER_CENTER, del_flag=FLAG_NO)
    internet_url = get_domain_name(user_center_obj.internet_url)
    return internet_url


def get_uc_internal_domain_list():
    user_center_obj = Service.objects.get(code=settings.SERVICE_USER_CENTER, del_flag=FLAG_NO)
    if "[" in user_center_obj.intranet_url:
        ret_domain_list = []
        domain_list = json.loads(user_center_obj.intranet_url)
        for domain in domain_list:
            ret_domain_list.append(get_domain_name(domain))
        return ret_domain_list
    else:
        intranet_url = get_domain_name(user_center_obj.intranet_url)
        return [intranet_url]


def api_detail_account(user, username=""):
    account_id = user.id
    school_id = user.school_id
    user_type = user.type
    ret_list = []
    if user_type == USER_TYPE_STUDENT:
        student_list = Student.objects.filter(account_id=account_id, school_id=school_id, del_flag=FLAG_NO).\
            values("id", "full_name", "school_id", "school__name_full", "school__name_simple", "image_url")
        for student in student_list:
            school_name = student["school__name_simple"]
            if not school_name:
                school_name = student["school__name_full"]
            image_url = ""
            if student["image_url"]:
                image_url = get_image_url(student["image_url"])
            user_type = dict(type_id=str(USER_TYPE_STUDENT), type_name=u"学生", school_id=str(student["school_id"]),
                             school_name=school_name, full_name=student["full_name"],
                             id=str(student["id"]), account_id=str(account_id), image_url=image_url)
            ret_list.append(user_type)

    elif user_type == USER_TYPE_PARENT:
        parent_list_ = Parent.objects.filter(account_id=account_id, del_flag=FLAG_NO).\
            values("id", "full_name", "school_id", "school__name_full", "school__name_simple", "image_url")
        for parent in parent_list_:
            school_name = parent["school__name_simple"]
            if not school_name:
                school_name = parent["school__name_full"]
            image_url = ""
            if parent["image_url"]:
                image_url = get_image_url(parent["image_url"])
            user_type = dict(type_id=str(USER_TYPE_PARENT), type_name=u"家长", school_id=str(parent["school_id"]),
                             school_name=school_name, full_name=parent["full_name"],
                             id=str(parent["id"]), account_id=str(account_id), image_url=image_url)
            ret_list.append(user_type)
    elif user_type == USER_TYPE_TEACHER:
        teacher_list = Teacher.objects.filter(account_id=account_id, del_flag=FLAG_NO).\
            values("id", "full_name", "school_id", "school__name_full", "school__name_simple", "image_url")
        for teacher in teacher_list:
            school_name = teacher["school__name_simple"]
            if not school_name:
                school_name = teacher["school__name_full"]
            image_url = ""
            if teacher["image_url"]:
                image_url = get_image_url(teacher["image_url"])
            user_type = dict(type_id=str(USER_TYPE_TEACHER), type_name=u"教师", school_id=str(teacher["school_id"]),
                             school_name=school_name, full_name=teacher["full_name"],
                             id=str(teacher["id"]), account_id=str(account_id), image_url=image_url)
            ret_list.append(user_type)

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_list}


# ---------------------------------------------------------------
# add common api
def get_teacher_title_name(title_name, cls_id):
    if cls_id:
        if title_name:
            if title_name == TITLE_NAME_TEACHER:
                title_name = ''
            else:
                title_name += u"、"
        else:
            title_name = ''
        title_name += TITLE_NAME_CLASSMASTER
    return title_name


# ----------------------------------------------------------------
# api added in teacher_resources, and communicate with user center
def school_list_textbook(user, subject_id_list=[], grade_num_list=[]):
    school_id = user.school_id
    if subject_id_list:
        subject_id_list = map(lambda x: int(x), subject_id_list)
    if grade_num_list:
        grade_num_list = map(lambda x: int(x), grade_num_list)

    textbook_id_list = SchoolTextbook.objects.filter(school_id=school_id, del_flag=0).values_list("textbook_id", flat=True)

    textbook_id_list = list(textbook_id_list)

    textbook_list = Textbook.objects.filter(id__in=textbook_id_list, is_active=1, subject__is_active=1, del_flag=0).all()

    if grade_num_list:
        textbook_list = textbook_list.filter(grade_num__in=grade_num_list)

    if subject_id_list:
        textbook_list = textbook_list.filter(subject_id__in=subject_id_list)

    textbook_info_list = textbook_list.order_by("grade_num", "subject_id").values("id", "grade_num", "subject__name", "name")

    ret_textbook_list = []
    for textbook_info in textbook_info_list:
        ret_textbook = dict( id=str(textbook_info["id"]),
                             grade_num=str(textbook_info["grade_num"]),
                             subject_name=textbook_info["subject__name"],
                             textbook_name=textbook_info["name"],
                           )
        ret_textbook_list.append(ret_textbook)

    dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_textbook_list}
    return dict_resp


def list_teacher_textbook(user, teacher_id="", subject_id=""):
    if teacher_id:
        return {"c": ERR_USER_AUTH[0], "m": ERR_USER_AUTH[1], "d": []}
    else:
        teacher_id = Teacher.objects.filter(account_id=user.id, school_id=user.school_id, del_flag=FLAG_NO).first()

    school_textbook_id_list = SchoolTextbook.objects.filter(school_id=user.school_id, del_flag=FLAG_NO,
                                                            textbook__is_active=FLAG_YES, textbook__del_flag=FLAG_NO,
                                                            textbook__subject__is_active=FLAG_YES).\
        values_list("textbook_id", flat=True)
    textbook_list = TeacherTextbook.objects.filter(teacher_id=teacher_id,
                                                   textbook_id__in=school_textbook_id_list,
                                                   del_flag=FLAG_NO)

    if subject_id:
        textbook_list = textbook_list.filter(textbook__subject_id=int(subject_id))
    textbook_list = textbook_list.values("textbook_id", "textbook__name", "textbook__subject__name", "is_current")
    textbook_list = list(textbook_list)
    ret_textbook_list = []
    for textbook_info in textbook_list:
        ret_textbook_info = {"textbook_id": textbook_info["textbook_id"],
                             "textbook_name": textbook_info["textbook__name"],
                             "is_current": textbook_info["is_current"],
                             "subject_name": textbook_info["textbook__subject__name"]}
        ret_textbook_list.append(ret_textbook_info)
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_textbook_list}


def admin_list_chapter(user, textbook_id=""):
    if not textbook_id:
        return {"c": ERR_TEXTBOOK_ID_ERROR[0], "m": ERR_TEXTBOOK_ID_ERROR[1], "d": []}

    textbook_id = int(textbook_id)

    textbook_obj = Textbook.objects.filter(id=textbook_id, is_active=1, del_flag=0).first()

    if not textbook_obj:
        return {"c": ERR_TEXTBOOK_ID_ERROR[0], "m": ERR_TEXTBOOK_ID_ERROR[1], "d": []}

    chapter_info_list = list(Chapter.objects.filter(textbook_id=textbook_id, del_flag=0).order_by("parent_id", "-sn")\
                                 .values("id", "parent_id", "sn", "name"))

    #将章节的ID按照关系排序
    chapter_id_list = []
    for chapter_info in chapter_info_list:
        if chapter_info["parent_id"] is None:
            index = 0
        else:
            index = chapter_id_list.index(chapter_info["parent_id"]) + 1
        chapter_id_list.insert(index, chapter_info["id"])


    ret_chapter_list = []
    for chapter_id in chapter_id_list:
        for chapter_info in chapter_info_list:
            if chapter_id == chapter_info["id"]:
                if chapter_info["parent_id"] is None:
                    chapter_info["parent_id"] = 0
                ret_chapter = dict(  id=chapter_info["id"],
                                     pId=chapter_info["parent_id"],
                                     name=chapter_info["name"],
                                     sn=chapter_info["sn"]
                                  )
                ret_chapter_list.append(ret_chapter)
                chapter_info_list.remove(chapter_info)
                break

    dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_chapter_list}
    return dict_resp


def school_list_subject(user):
    school_id = user.school_id

    subject_info_list = SchoolSubject.objects.filter(school_id=school_id, subject__is_active=1, subject__del_flag=0, del_flag=0)\
                                                           .order_by("-update_time").values("subject_id", "subject__name")

    ret_subject_list = []
    for subject_info in subject_info_list:
        ret_subject = dict(  id=str(subject_info["subject_id"]),
                             name=subject_info["subject__name"],
                          )
        ret_subject_list.append(ret_subject)

    dict_resp = {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_subject_list}
    return dict_resp

def list_title(user, exclude_class_master=""):
    school_id = user.school_id
    teacher_id_list = Teacher.objects.filter(school_id=school_id, title_id__isnull=False, del_flag=FLAG_NO,
                                             is_in=True).values("id", "title_id")
    teacher_title_dict = convert_list_to_dict(teacher_id_list, "title_id")
    title_list = Title.objects.filter(school_id=school_id, del_flag=FLAG_NO)
    ret_title_list = []
    for title in title_list:
        if title.id in teacher_title_dict.keys() and title.teacher_amount != len(teacher_title_dict[title.id]):
            title.teacher_amount = len(teacher_title_dict[title.id])
            title.save()
        ret_title = {"id": title.id, "name": title.name, "comments": title.comments, "teacher_amount": title.teacher_amount}
        if not ret_title["comments"]:
            ret_title["comments"] = u"自定义类型"
        if exclude_class_master and int(exclude_class_master) == FLAG_YES and title.name == TITLE_NAME_CLASSMASTER:
            continue
        ret_title_list.append(ret_title)

    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": ret_title_list}