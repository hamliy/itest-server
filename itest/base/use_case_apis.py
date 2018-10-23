#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/9/2 下午7:15
# @Author  : lihan
# @File    : use_case_apis.py
# @Dec     :
"""
    接口基本功能api：
    1、查看全部
    2、根据id查看
    3、新增
    4、修改
    5、删除
"""

from flask import Blueprint, request
from itest.models import UseCase, Project
from bson import ObjectId
from itest.utils.utils import init_return, mongo_to_dict, get_value
from itest.utils.decorators import params_required, params_objectid_check, project_check, params_empty_check
import json

blueprint = Blueprint('usecase', __name__)


@blueprint.route('/all', methods=['GET', 'POST'])
@params_objectid_check(['project_id'])
@params_required(['project_id'])
def all_use_cases():
    """
     1 获取所有测试用例信息接口,根据项目
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    page = 1
    page_size = 20
    project_id = data['project_id']

    if 'page' in data and 'page_size' in data:
        page = data['page']
        page_size = data['page_size']

    use_cases = UseCase.objects(project=ObjectId(project_id))[page_size * (page - 1):page_size * page]
    total = UseCase.objects(project=ObjectId(project_id)).count()
    data = []
    for use_case in use_cases:
        data.append(mongo_to_dict(use_case))
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)


@blueprint.route('/<use_case_id>', methods=['GET', 'POST'])
def get_use_case(use_case_id):
    """
     2、根据id查看
    :param: use_case_id
    :return:
    """
    use_case = UseCase.objects(id=ObjectId(use_case_id))
    if use_case.count() == 0:
        return init_return({}, sucess=False, error="查找的用例不存在", errorCode=1001)
    else:
        return init_return(mongo_to_dict(use_case.first()))


@blueprint.route('/add', methods=['GET', 'POST'])
@project_check
@params_required(['project_id', 'name', 'request', 'params', 'expect'])
def add():
    """
      3 新增接口
    :return:
    """
    data = request.get_json()

    project_id = data['project_id']
    name = data['name']
    use_case_request = data['request']
    if 'interface' in use_case_request and use_case_request['interface'] and ObjectId.is_valid(use_case_request['interface']):
        use_case_request['interface'] = ObjectId(use_case_request['interface'])

    expect = get_value(data, 'expect', {})
    params = get_value(data, 'params', [])
    rule = get_value(data, 'rule', {})
    description = get_value(data, 'description')

    existed = UseCase.objects(name=name, project=ObjectId(project_id)).first()
    if existed:
        return init_return({}, sucess=False, error="存在相同用例名", errorCode=1001)

    UseCase(name=name, project=ObjectId(project_id), request=use_case_request, params=params,
            expect=expect, rule=rule, remarks={'description': description}).save()
    return init_return({
        'data': '新增成功'
    })


@blueprint.route('/update', methods=['GET', 'POST'])
@params_required(['id', 'name'])
def update():
    """
      4 根据用例id更新接口
    :return:
    """
    data = request.get_json()
    id = data['id']
    name = data['name']

    use_case = UseCase.objects(id=ObjectId(id))
    if use_case.count() == 0:
        return init_return({}, sucess=False, error="更新的用例不存在", errorCode=1001)
    else:
        existed = UseCase.objects(name=name, project=use_case.first().project).first()
        if existed and str(existed.id) != id:
            return init_return({}, sucess=False, error="存在相同的用例名", errorCode=1001)

        use_case_request = get_value(data, 'request', [])
        if 'interface' in use_case_request and ObjectId.is_valid(use_case_request['interface']):
            use_case_request['interface'] = ObjectId(use_case_request['interface'])
        expect = get_value(data, 'expect', {})
        params = get_value(data, 'params', [])
        rule = get_value(data, 'rule', {})
        description = get_value(data, 'description')

        source = mongo_to_dict(use_case.first())

        if name != source['name']:
            use_case.update_one(name=name)
        if use_case_request != source['request']:
            use_case.update_one(request=use_case_request)
        if expect != source['expect']:
            use_case.update_one(expect=expect)
        if params != source['params']:
            use_case.update_one(params=params)
        if rule != source['rule']:
            use_case.update_one(rule=rule)
        if description != source['remarks']['description']:
            use_case.update_one(remarks__description=description)

        return init_return({
            'data': '更新成功'
        })


@blueprint.route('/delete/<use_cace_id>', methods=['GET', 'POST'])
def delete(use_cace_id):
    """
     5 根据用例id
    :param: use_cace_id
    :return:
    """
    if not ObjectId.is_valid(use_cace_id):
        return init_return({}, sucess=False, error="用例id参数错误", errorCode=1001)

    result = UseCase.objects(id=ObjectId(use_cace_id)).delete()
    if result == 0:
        return init_return({}, sucess=False, error="删除的用例不存在", errorCode=1001)
    else:
        return init_return({'data': '删除成功'})