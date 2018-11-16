# encoding: utf-8
"""
@author: han.li
@file  : a_mark_field.py
@time  : 11/14/18 8:16 PM
@dec   : 定义标签字段
"""

from flask import Blueprint, request
from itest.service.mark.s_mark_field import MarkFieldService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params

blueprint = Blueprint('mark-field', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'project_id'], empty_check_params=['project_id'])
def search():
    info = request.get_json()
    data = MarkFieldService.find(info['query'], info['project_id'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = MarkFieldService.get_marks(request.args.get('projectId'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['projectId', 'name', 'fieldType', 'fieldItems', 'desc'],
             empty_check_params=['projectId', 'fieldType', 'name'])
def create():
    info = request.get_json()
    data = MarkFieldService.create(info)
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'name', 'fieldType', 'fieldItems', 'desc'],
             empty_check_params=['id', 'fieldType', 'name'])
def update():
    info = request.get_json()
    rs, status = MarkFieldService.update(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此标签字段，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = MarkFieldService.delete(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此标签字段，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    return init_return(rs)
