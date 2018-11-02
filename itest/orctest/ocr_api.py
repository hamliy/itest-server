# encoding: utf-8
"""
@author: han.li
@file  : ocr_api.py
@time  : 11/1/18 4:42 PM
@dec   : 
"""
from flask import Blueprint, request
from bson import ObjectId
import random, string, os

from itest.utils.utils import init_return, convert_mongo_to_json, get_images_path
from itest.utils.img_util import return_img_stream
from itest.utils.decorators import params_required, params_objectid_check
import uuid

blueprint = Blueprint('ocr', __name__)

# 金蝶ocr识别
@blueprint.route('/ocr/ko', methods=['POST'])
def orc_ko():
    """
    获取所有图片数据
    :return:
    """
    data = request.get_json()
    project_id = data['project_id']
    page = data['page']
    page_size = data['page_size']
    data = []
    for image in images:
        print(image)
        data.append(convert_mongo_to_json(image))
    info = {
        "total": total,
        "data": data
    }
    return init_return(info)

# 百度ocr识别
@blueprint.route('/ocr/bo', methods=['POST'])
def orc_bo():
    """
    获取所有图片数据
    :return:
    """
    data = request.get_json()
    project_id = data['project_id']
    page = data['page']
    page_size = data['page_size']
    data = []
    for image in images:
        print(image)
        data.append(convert_mongo_to_json(image))
    info = {
        "total": total,
        "data": data
    }
    return init_return(info)
