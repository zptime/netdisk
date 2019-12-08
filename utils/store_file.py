# -*- coding: utf-8 -*-

import logging
import os
import io

import datetime
import random

from PIL import Image
from django.conf import settings


logger = logging.getLogger(__name__)


def filename_unique(fname):
    (shortname, extension) = os.path.splitext(fname)
    return '%s_%s%s' % (shortname, guid_by_time(), extension)


def create_crop(raw_file, crop_tmp_path):
    try:
        pil_image = Image.open(raw_file)
        width, height = pil_image.size
        length = min(width, height, settings.PICTURE_CROP_WIDTH)

        left = (width - length) / 2
        top = (height - length) / 2
        right = (width + length) / 2
        bottom = (height + length) / 2

        cropped = pil_image.crop((left, top, right, bottom))
        cropped.save(crop_tmp_path)
        logger.info('create picture crop successful, here: ' + crop_tmp_path)
        return True
    except IOError as ioe:
        logger.exception('create picture crop fail, maybe it is not a image: ' + raw_file)
        return False
    except Exception as e:
        logger.error('create picture crop fail: ' + raw_file)
        logger.exception(e)
        return False


def create_thumb(raw_file, save_path):
    """
    生成图片缩略图
    :param image_file: 原图片文件
    :param save_path: 缩略图临时保存地点
    :return: 生成了缩略图则返回True，不需要生成或者未生成则返回False
    """
    try:
        pil_image = Image.open(raw_file)
        width, height = pil_image.size
        if width > settings.PICTURE_NEED_THUMB_WIDTH or height > settings.PICTURE_NEED_THUMB_HEIGHT:
            # PIL会等比缩放到长与宽都小于指定值
            pil_image.thumbnail((settings.PICTURE_NEED_THUMB_WIDTH, settings.PICTURE_NEED_THUMB_HEIGHT), Image.ANTIALIAS)
            pil_image.save(save_path, settings.PICTURE_THUMB_FORMAT)
            logger.info('create picture thumb successful, here: ' + save_path)
            return True
        logger.info('no need to picture thumb for' + save_path)
        return False
    except IOError as ioe:
        logger.exception('create picture crop fail, maybe it is not a image: ' + raw_file)
        return False
    except Exception as e:
        logger.exception('create picture thumb fail: ' + raw_file)
        return False


def touch(file_path, times=None):
    with open(file_path, 'a'):
        os.utime(file_path, times)


def must_exist_folder(path):
    """  
        确保文件夹存在
    """
    if not os.path.exists(path):
        logger.info('create folder: ' + path)
        os.makedirs(path)
    return path


def must_exist_file(path):
    """  
        确保文件存在
    """
    if not os.path.exists(path):
        touch(path)
    return path


def save_file(file_stream, save_path):
    # 需要file_stream支持chunks，例如使用filechunkio
    with open(save_path, 'wb+') as w:
        for chunk in file_stream.chunks():
            w.write(chunk)


def fdelete(path):
    if os.path.exists(path):
        os.remove(path)


def safe_folder(path):
    if not os.path.exists(path):
        logger.info('create folder: ' + path)
        os.makedirs(path)
    return path


def gen_path(path, filename, absolute=False):
    final_path = os.path.join(safe_folder(path), filename)
    if absolute:
        return os.path.join(settings.BASE_DIR, final_path)
    else:
        return final_path


def gen_thumb_fname(image_fname):
    return os.path.splitext(image_fname)[0] + '_thumb.' + settings.PICTURE_THUMB_FORMAT


def gen_crop_fname(image_fname):
    return os.path.splitext(image_fname)[0] + '_crop.' + settings.PICTURE_THUMB_FORMAT


def guid_by_time():
    """
        通过当前时间生成唯一标识符(20位)
    """
    fn = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
    fn += '%d' % random.randint(10, 99)
    return fn
