# encoding: utf-8
"""
@author: han.li
@file  : a_interface.py
@time  : 11/15/18 2:08 PM
@dec   : 接口相关请求
"""

from flask import Blueprint, request
from itest.service.interface.s_interface import InterfaceService
from itest.service.interface.s_interface_group import InterfaceGroupService
from itest.service.interface.s_interface_history import InterfaceHistoryService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params

blueprint = Blueprint('interfaces', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'projectId'], empty_check_params=['projectId'])
def search():
    info = request.get_json()
    data = InterfaceService.find(info['query'], info['projectId'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = InterfaceService.get_interfaces(request.args.get('projectId'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['projectId', 'groupId', 'option', 'name', 'desc'],
             empty_check_params=['projectId', 'groupId', 'name', 'option'])
def create():
    info = request.get_json()
    group, status = InterfaceGroupService.get_by_id(info['groupId'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此接口，请确认", errorCode=3005)

    data = InterfaceService.create(info)
    InterfaceGroupService.add_member(info['groupId'], data['id'])
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'name', 'desc', 'option'], empty_check_params=['id', 'name', 'option'])
def update():
    info = request.get_json()
    current_interface = InterfaceService.get_by_id(info['id'])
    rs, status = InterfaceService.update(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此接口，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)

    rs['history'] = InterfaceHistoryService.push(current_interface)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = InterfaceService.delete(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此接口，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    InterfaceGroupService.delete_member(rs['groupId'], info['id'])
    return init_return(rs)
