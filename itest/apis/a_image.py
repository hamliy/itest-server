# encoding: utf-8
"""
@author: han.li
@file  : a_image.py
@time  : 11/14/18 11:04 AM
@dec   : 图片接口
"""

from flask import Blueprint, request
from itest.service.image.s_image import ImageService
from itest.service.image.s_image_group import ImageGroupService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params

blueprint = Blueprint('images', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'project_id'], empty_check_params=['project_id'])
def search():
    info = request.get_json()
    data = ImageService.find(info['query'], info['project_id'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = ImageService.get_images(request.args.get('project_id'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)


@blueprint.route('/create', methods=['POST'])
# @init_params(params=['projectId', 'name', 'image_type', 'desc'], empty_check_params=['projectId', 'name','image_type'])
def create():
    request_data = request.form
    image_name = request_data.get('name')
    image_type = int(request_data.get('imageType'))
    desc = request_data.get('desc')
    tags = request_data.get('tags').strip().split(',');
    project_id = request_data.get('projectId')
    group_id = request_data.get('groupId')
    info = {
        'name': image_name,
        'imageType': image_type,
        'desc': desc,
        'tags': tags,
        'groupId': group_id,
        'projectId': project_id
    }
    # 获取图片文件
    upload = request.files.get('file')
    if not upload:
        return init_return({}, sucess=False, error="请上传图片", errorCode=4001)

    image_path, status = ImageService.save_image(upload)
    if status == 'ext_error':
        return init_return({}, sucess=False, error="图片类型错误", errorCode=4002)
    info['path'] = image_path
    data = ImageService.create(info)
    ImageGroupService.add_member(info['groupId'], data['id'])
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'name', 'imageType', 'tags', 'desc'],
             empty_check_params=['id', 'name', 'imageType'])
def update():
    info = request.get_json()
    rs, status = ImageService.update(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此图片，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/update-marks', methods=['POST'])
@init_params(params=['id', 'marks'], empty_check=True)
def update_marks():
    info = request.get_json()
    rs, status = ImageService.update_marks(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此图片，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = ImageService.delete(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此图片，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    return init_return(rs)