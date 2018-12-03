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
    rs = InterfaceService.get_by_id(request.args.get('interfaceId'))
    # if status == 'not_object_id':
    #     return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)


@blueprint.route('/group-tree', methods=['GET', 'POST'])
@init_params(params=['projectId'], empty_check=True)
def get_group_interface():
    """
    获取接口分组+接口树
    :return:
    """
    info = request.get_json()
    tree = InterfaceService.get_group_interface(info['projectId'])
    return init_return(tree)


@blueprint.route('/group', methods=['GET', 'POST'])
def get_interface_by_group():
    """
    获取接口分组接口列表
    :return:
    """

    data = InterfaceService.get_by_group_id(request.args.get('groupId'))
    return init_return(data)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['projectId', 'groupId', 'option', 'method', 'path', 'name', 'desc'],
             empty_check_params=['projectId', 'groupId', 'method', 'path', 'name', 'option'])
def create():
    info = request.get_json()
    group, status = InterfaceGroupService.get_by_id(info['groupId'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此接口，请确认", errorCode=3005)

    data = InterfaceService.create(info)
    InterfaceGroupService.add_member(info['groupId'], data)
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
    # 如果修改了接口名，更新接口组存储接口名信息
    if current_interface['name'] != info['name']:
        InterfaceGroupService.update_interface_name(info['groupId'], info['id'], info['name'])
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
