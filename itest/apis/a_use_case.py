# encoding: utf-8
"""
@author: han.li
@file  : a_test_case.py
@time  : 2/28/19 4:26 PM
@dec   : 用例接口
"""

from flask import Blueprint, request
from itest.service.test_case.s_test_case import TestCaseService
from itest.utils.utils import init_return, get_test_dir_path
from itest.utils.runner import run_test_by_type, run_by_batch
from itest.utils.decorators import init_params
from itest.celery_tasks import main_hrun


blueprint = Blueprint('use_case', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query', 'page', 'pageSize'])
def search():
    info = request.get_json()
    data = TestCaseService.find(info['query'], info['page'], info['pageSize'])
    return init_return(data)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    data = TestCaseService.get_test_cases()
    return init_return(data)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['name', 'configType', 'projectId', 'moduleId', 'level', 'include', 'request', 'desc'],
             empty_check_params=['name', 'configType', 'projectId', 'moduleId', 'level', 'include', 'request'])
def create():
    info = request.get_json()
    is_exist = TestCaseService.get_by_name(info['name'])
    if is_exist:
        return init_return({}, sucess=False, error="用例名已被使用", errorCode=3001)

    data = TestCaseService.create(info)
    return init_return(data)


@blueprint.route('/update', methods=['POST'])
@init_params(params=['id', 'name', 'configType','include', 'level', 'request', 'desc'],
             empty_check_params=['id', 'name', 'configType','include', 'level', 'request'])
def update():
    info = request.get_json()
    rs, status = TestCaseService.update(info)
    if status == 'not_unique':
        return init_return({}, sucess=False, error="用例名重复，修改失败", errorCode=3002)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="用例id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此用例，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=3004)
    return init_return(rs)


@blueprint.route('/delete', methods=['POST'])
@init_params(params=['id'], empty_check=True)
def delete():
    info = request.get_json()
    rs, status = TestCaseService.delete(info['id'])
    if status == 'not_unique':
        return init_return({}, sucess=False, error="用例名重复，删除失败", errorCode=3002)
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="用例id不存在", errorCode=3003)
    if status == 'not_find':
        return init_return({}, sucess=False, error="查无此用例，请确认", errorCode=3005)
    if not rs:
        return init_return({}, sucess=False, error="删除用例失败", errorCode=3006)
    return init_return(rs)


@blueprint.route('/run_test', methods=['POST'])
@init_params(params=['id', 'reportName', 'envName', 'type'], empty_check=['id', 'envName', 'type'])
def run_test():
    info = request.get_json()
    id = info['id']
    base_url = info['envName']
    type = info['type']
    test_dir_path = get_test_dir_path(type)
    # 生成测试用例文件
    run_test_by_type(id, base_url, test_dir_path, type)

    report_name = info['reportName']
    # 异步运行
    main_hrun.delay(test_dir_path, report_name)
    return init_return('用例执行中，请稍后查看')


@blueprint.route('/run_batch_test', methods=['POST'])
@init_params(params=['ids', 'reportName', 'envName', 'type'], empty_check=['ids', 'envName', 'type'])
def run_batch_test():
    info = request.get_json()
    test_list = info['ids']
    base_url = info['envName']
    type = info['type']
    test_dir_path = get_test_dir_path(type)
    # 生成测试用例文件
    run_by_batch(test_list, base_url, test_dir_path, type)

    report_name = info['reportName']
    # 异步运行
    main_hrun.delay(test_dir_path, report_name)
    return init_return('用例执行中，请稍后查看')


