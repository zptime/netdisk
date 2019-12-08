# -*- coding=utf-8 -*-
from django.conf import settings
from models import *
from agents import get_uc_internal_domain_list
from utils import *
import logging
import sys

logger = logging.getLogger(__name__)


def class_name_to_class(model_cls_name):
    model_cls = getattr(sys.modules[__name__], model_cls_name)
    return model_cls


def clear_table(model_name, clean_all=False):
    # 获取该表对应的类对象
    model_cls = class_name_to_class(model_name)
    if clean_all:
        model_cls.objects.filter().delete()
    else:
        model_cls.objects.filter(del_flag=FLAG_YES).delete()


def refresh_table(model_name, ignore_update_time=False, uc_domain=None):
    # 获取该表对应的类对象
    model_cls = class_name_to_class(model_name)

    local_update_time = datetime.datetime(year=1970, month=1, day=1)
    if ignore_update_time:
        model_cls.objects.update(update_time=local_update_time)
    while True:
        # 获取本地最后更新的数据
        obj = model_cls.objects.all().order_by("-update_time", "-id").first()
        item_id = 0
        if obj:
            local_update_time = obj.update_time
            item_id = obj.id
        local_update_time = convert_datetime_to_str(local_update_time, DATE_FORMAT_TIME)
        # url = settings.USER_CENTER_URL + settings.API_USER_CENTER_LIST_ITEMS
        if uc_domain:
            domain_list = [uc_domain]
        else:
            domain_list = get_uc_internal_domain_list()
        form_data_dict = {"model_name": model_name, "update_time": local_update_time, "item_id": item_id}
        response = try_send_http_request(domain_list=domain_list, path=settings.API_USER_CENTER_LIST_ITEMS,
                                         method="POST", form_data_dict=form_data_dict)
        response_dict = json.loads(response, cls=RoundTripDecoder)
        if response_dict["c"] != ERR_SUCCESS[0]:
            logger.error("list_items %s" % response_dict["m"])
            return
        item_list = response_dict["d"]
        logger.info("[refresh_table] %s %s item_id(%s) len(%s)" % (model_name, local_update_time, item_id, len(item_list)))
        if not item_list:
            break

        # 创建或更新本地表格数据
        for item in item_list:
            try:
                obj = model_cls.objects.get(id=item["id"])
                for key, value in item.items():
                    setattr(obj, key, value)
                obj.save()
            except model_cls.DoesNotExist:
                obj = model_cls(**item)
                obj.save()


def refresh_all_tables(ignore_update_time=False):
    for model_name in settings.MODEL_SYNC_FROM_USER_CENTER:
        refresh_table(model_name, ignore_update_time)


def refresh_item(model_name, item_id, item_data):
    # 获取该表对应的类对象
    model_cls = class_name_to_class(model_name)
    item_id = int(item_id)
    item_data = json.loads(item_data, cls=RoundTripDecoder)
    item_obj = model_cls.objects.filter(id=item_id).first()
    if not item_obj:
        return {"c": ERR_ITEM_NOT_EXIST[0], "m": ERR_ITEM_NOT_EXIST[1], "d": []}
    for key, value in item_data.items():
        setattr(item_obj, key, value)
    item_obj.save()
    return {"c": ERR_SUCCESS[0], "m": ERR_SUCCESS[1], "d": []}
