# -*- coding=utf-8 -*-

import logging


logger = logging.getLogger(__name__)


def remove_dup_in_dictlist(dictlist, keys_list):
    """
        去掉字典列表中的指定组合关键字重复的记录
    """
    remove_dup_list = list()
    result_list = list()
    for element in dictlist:
        tp = sorted((element[each_key] for each_key in keys_list))
        if tp not in remove_dup_list:
            result_list.append(element)
            remove_dup_list.append(tp)
    return result_list


def dictlist_sort(dictlist, cond):
    """
        字典列表排序，可指定按照不同字段的排序、优先级、是否按照数值排序等，目前支持字典value是字符串或者整型
        condiction = [  # 优先级从高到低， 'as_int'表示该字段是否按照整型排序
            {'key': 'a', 'sort': 'ASC'},
            {'key': 'b', 'sort': 'ASC'},
            {'key': 'c', 'sort': 'DESC', 'as_int': True},
        ]
        test_case_dictlist = [
            {'a': 'a01', 'b': 'b01', 'c': '5'},
            {'a': 'a01', 'b': 'b01', 'c': '20'},
            {'a': 'a03', 'b': 'b03', 'c': '4'},
            {'a': 'a02', 'b': 'b03', 'c': '5'},
            {'a': 'a02', 'b': 'b07', 'c': '3'},
            {'a': 'a03', 'b': 'b04', 'c': '15'},
            {'a': 'a01', 'b': 'b01', 'c': '10'},
        ] 
        排序结果：
        [
            {'a': 'a01', 'c': '20', 'b': 'b01'}, 
            {'a': 'a01', 'c': '10', 'b': 'b01'}, 
            {'a': 'a01', 'c': '5', 'b': 'b01'}, 
            {'a': 'a02', 'c': '5', 'b': 'b03'}, 
            {'a': 'a02', 'c': '3', 'b': 'b07'}, 
            {'a': 'a03', 'c': '4', 'b': 'b03'}, 
            {'a': 'a03', 'c': '15', 'b': 'b04'}
        ]
        或使用多次排序亦可：
        test_case_dictlist.sort(key=lambda x: int(x['c']))
        test_case_dictlist.sort(key=itemgetter('a', 'b'))
    """
    def need_reservse(string):
        return True if string == 'DESC' else False

    def get_comp_item(item, cond):
        if cond.get('as_int', False):
            try:
                value = int((item.get(cond['key'], 0)))
            except ValueError as e:
                value = item.get(cond['key'], '')
        else:
            value = item.get(cond['key'], '')
        return value

    cond.reverse()
    for each_cond in cond:
        dictlist.sort(key=lambda item: get_comp_item(item, each_cond),
                       reverse=need_reservse(each_cond['sort']))


def remove_dup_in_dictlist(raw_list, key):
    """
        从字典型列表中去除指定关键字重复的记录
    """
    result = list()
    key_bucket = list()
    for each in raw_list:
        if each[key] in key_bucket:
            continue
        else:
            result.append(each)
            key_bucket.append(each[key])
    return result

