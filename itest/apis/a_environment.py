# encoding: utf-8
"""
@author: han.li
@file  : a_environment.py
@time  : 11/15/18 10:07 AM
@dec   : 环境接口
"""

from flask import Blueprint, request
from itest.service.environment.s_environment import EnvironmentService
from itest.utils.utils import init_return
from itest.utils.decorators import init_params

blueprint = Blueprint('envs', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'page', 'pageSize','projectId'], empty_check_params=['projectId'])
def search():
    info = request.get_json()
    data = EnvironmentService.find(info['query'], info['projectId'], info['page'], info['pageSize'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = EnvironmentService.get_envs(request.args.get('project_id'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="项目id不存在", errorCode=3003)
    return init_return(rs)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['projectId', 'port', 'protocol', 'ip', 'name', 'desc'],
             empty_check_params=['projectId', 'ip', 'protocol', 'port', 'name'])
def create():
    info = request.get_json()
    data = EnvironmentService.create(info)
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'port', 'protocol', 'ip', 'name', 'desc'],
             empty_check_params=['id', 'ip', 'protocol', 'port', 'name'])
def update():
    info = request.get_json()
    rs, status = EnvironmentService.update(info)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="环境id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此环境，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = EnvironmentService.delete(info['id'])
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="环境id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此环境，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除失败", errorCode=3006)
    return init_return(rs)

