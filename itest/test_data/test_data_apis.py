# encoding: utf-8
"""
@author: han.li
@file  : test_data_apis.py
@time  : 8/15/18 4:29 PM
@dec   : 测试数据接口
"""
from flask import Blueprint, request
from .models import ImageData
from bson import ObjectId
import random, string, os

from itest.utils.utils import init_return, convert_mongo_to_json, get_images_path
from itest.utils.img_util import return_img_stream
from itest.utils.decorators import params_required, params_objectid_check
import uuid

blueprint = Blueprint('data', __name__)

# 图片相关接口
@blueprint.route('/images/query', methods=['POST'])
def query_images_data():
    """
    获取所有图片数据
    :return:
    """
    data = request.get_json()
    project_id = data['project_id']
    page = data['page']
    page_size = data['page_size']

    images = ImageData.objects(project_id=ObjectId(project_id))[page_size * (page - 1):page_size * page]
    total = ImageData.objects(project_id=ObjectId(project_id)).count()
    data = []
    for image in images:
        print(image)
        data.append(convert_mongo_to_json(image))
    info = {
        "total": total,
        "data": data
    }
    return init_return(info)


@blueprint.route('/images/get/', methods=['GET'])
# @params_objectid_check(['image_id'])
# @params_required(['image_id'])
def get_image():
    """
     2、根据id查看
    :param: image_id
    :return:
    """
    data = request.args
    image_id = data.get('image_id')
    image = ImageData.objects(id=ObjectId(image_id)).first()
    image_json = convert_mongo_to_json(image)
    image_path = image_json['image_path']
    if image_json and image_json != {}:
        print(return_img_stream(image_path))
        return init_return(return_img_stream(image_path))
    else:
        return init_return({}, sucess=False, error="查看的图片不存在", errorCode=1001)


@blueprint.route('/images/create', methods=['POST'])
# @params_objectid_check(['project_id'])
# @params_required(['project_id', 'request_data'])
def images_create():
    """
     7 获取所有接口主题信息接口,根据项目
    :return:
    """
    request_data = request.form
    image_name = request_data.get('image_name')
    image_type = int(request_data.get('image_type'))
    tags = [request_data.get('tags')]
    marks = []
    desc = request_data.get('desc')
    project_id = request_data.get('project_id')
    # request_data = data['request_data']

    # 获取图片文件
    upload = request.files.get('file')
    print(upload)
    if not upload:
        return init_return({}, sucess=False, error="请上传图片", errorCode=1001)
    name, ext = os.path.splitext(upload.filename)
    if ext.lower() not in ('.png', '.jpg', '.jpeg'):
        return init_return({}, sucess=False, error="图片类型错误", errorCode=1001)
    # 定义一个图片存放的位置
    path = get_images_path()

    # 图片path和名称
    save_name = str(uuid.uuid1()) + ext
    image_path = os.path.join(path, save_name)

    # Create temporary directory for storing our files
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存图片
    upload.save(image_path, True)

    ImageData(project_id=ObjectId(project_id), image_name=image_name,image_path=image_path, image_type=image_type,
              tags=tags, marks=marks, desc=desc).save()
    return init_return({
        'data': '新增成功'
    })


@blueprint.route('/images/update', methods=['POST'])
def image_update():
    """
    更新图片基本信息
    图片名，图片类型，标签，对应数据集，备注 打标数据
    :return:
    """
    return ''

# 标签字段CRUD
# 接口请求

# 图片数据标签相关接口
@blueprint.route('/mark/field', methods=['POST'])
def mark_field():
    """
    标签字段定义
    图片名，图片类型，标签，对应数据集，备注
    :return:
    """
    return ''
