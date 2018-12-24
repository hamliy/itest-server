# encoding: utf-8
"""
@author: han.li
@file  : a_interface_use_case.py
@time  : 11/20/18 2:26 PM
@dec   : 用例相关
"""

from flask import Blueprint, request
from itest.service.interface_use_case.s_interface_use_case import InterfaceUseCaseService
from itest.service.interface_use_case.s_interface_use_case_group import InterfaceUseCaseGroupService
from itest.service.interface_use_case.s_interface_use_case_history import InterfaceUseCaseHistoryService
from itest.service.interface_use_case.s_interface_use_case_execute import InterfaceUseCaseExecuteService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params

blueprint = Blueprint('interface-use-case', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'page', 'pageSize', 'projectId'])
def search():
    info = request.get_json()
    data = InterfaceUseCaseService.find(info['query'], info['projectId'], info['page'], info['pageSize'])
    return init_return(data)


@blueprint.route('/getAll', methods=['GET', 'POST'])
@init_params(params=['projectId'], empty_check_params=['projectId'])
def getAll():
    info = request.get_json()
    rs, status = InterfaceUseCaseService.get_all(info['projectId'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)

@blueprint.route('/getById', methods=['GET', 'POST'])
def getById():
    rs = InterfaceUseCaseService.get_by_id(request.args.get('useCaseId'))
    return init_return(rs)

@blueprint.route('/getByGroupId', methods=['GET', 'POST'])
def getByGroupId():
    rs = InterfaceUseCaseService.get_by_group_id(request.args.get('useCaseGroupId'))
    return init_return(rs)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['projectId', 'interfaceId', 'groupId',
                     'level', 'options', 'name', 'desc'],
             empty_check_params=['projectId', 'interfaceId', 'groupId', 'name', 'options', 'groupId',
                                 'level', 'name'])
def create():
    info = request.get_json()
    group, status = InterfaceUseCaseGroupService.get_by_id(info['groupId'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="用例组id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此用例组，请确认", errorCode=3005)

    data, status2 = InterfaceUseCaseService.create(info)
    if status2 == 'not_object_id':
        return init_return({}, sucess=False, error="请求的object_id错误", errorCode=3003)
    if status2 == 'not_unique':
        return init_return({}, sucess=False, error="用例编号重复，请修改", errorCode=3007)
    InterfaceUseCaseGroupService.add_member(info['groupId'], data)
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'interfaceId', 'level', 'options', 'name', 'desc'],
             empty_check_params=['id',  'name', 'interfaceId', 'groupId',
                                 'level', 'options', 'name'])
def update():
    info = request.get_json()
    current_use_case = InterfaceUseCaseService.get_by_id(info['id'])
    rs, status = InterfaceUseCaseService.update(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="用例id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此接口，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)

    rs['history'] = InterfaceUseCaseHistoryService.push(current_use_case)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = InterfaceUseCaseService.delete(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="用例id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此接口，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    InterfaceUseCaseGroupService.delete_member(rs['groupId'], info['id'])
    return init_return(rs)


@blueprint.route('/execute', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def run_by_id():
    info = request.get_json()
    rs = InterfaceUseCaseExecuteService.execute_by_id(info['id'])
    return init_return(rs)


@blueprint.route('/execute/group', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def run_by_group():
    info = request.get_json()
    rs, status = InterfaceUseCaseExecuteService.execute_by_group(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="组id错误", errorCode=3003)
    return init_return(rs)
