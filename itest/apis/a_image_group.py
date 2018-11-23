# encoding: utf-8
"""
@author: han.li
@file  : a_image_group.py
@time  : 11/14/18 3:08 PM
@dec   : 图片分组接口
"""

from flask import Blueprint, request
from itest.service.image.s_image_group import ImageGroupService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params

blueprint = Blueprint('images-group', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'projectId'], empty_check_params=['projectId'])
def search():
    info = request.get_json()
    data = ImageGroupService.find(info['query'], info['projectId'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = ImageGroupService.get_groups(request.args.get('projectId'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['projectId', 'name', 'desc'], empty_check_params=['projectId', 'name'])
def create():
    info = request.get_json()
    data = ImageGroupService.create(info)
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'name', 'desc'], empty_check_params=['id', 'name'])
def update():
    info = request.get_json()
    rs, status = ImageGroupService.update(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此图片分组，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = ImageGroupService.delete(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此图片分组，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    return init_return(rs)
