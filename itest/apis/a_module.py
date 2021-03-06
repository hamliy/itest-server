# encoding: utf-8
"""
@author: han.li
@file  : a_module.py
@time  : 2/28/19 3:54 PM
@dec   : 模块管理
"""

from flask import Blueprint, request
from itest.service.module.s_module import ModuleService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params


blueprint = Blueprint('module', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'page', 'pageSize'])
def search():
    info = request.get_json()
    data = ModuleService.find(info['query'], info['page'], info['pageSize'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    data = ModuleService.get_modules()
    return init_return(data)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['name', 'projectId', 'testUser', 'desc'], empty_check_params=['name', 'projectId'])
def create():
    info = request.get_json()
    is_exist = ModuleService.get_by_name(info['name'])
    if is_exist:
        return init_return({}, sucess=False, error="项目名已被使用", errorCode=3001)

    data = ModuleService.create(info)
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'name', 'testUser', 'desc'], empty_check_params=['id', 'name'])
def update():
    info = request.get_json()
    rs, status = ModuleService.update(info)
    if status == 'not_unique':
        return init_return({}, sucess=False, error="项目名重复，修改失败", errorCode=3002)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此项目，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = ModuleService.delete(info['id'])
    if status == 'not_unique':
        return init_return({}, sucess=False, error="项目名重复，删除失败", errorCode=3002)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此项目，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    return init_return(rs)
