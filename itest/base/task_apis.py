#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/9/2 下午7:15
# @Author  : lihan
# @File    : project_api.py
# @Dec     : 

"""
    任务基本功能api：
    1、查看全部
    2、根据id查看
    3、新增
    4、修改
    5、删除
"""

from flask import Blueprint, request
from itest.models import Project, Task, Environment, TaskUseCase
from bson import ObjectId
from itest.utils.utils import init_return, mongo_to_dict, get_value
from itest.utils.decorators import params_required, params_objectid_check, project_check, params_empty_check
import json

blueprint = Blueprint('task', __name__)


@blueprint.route('/all', methods=['GET', 'POST'])
@params_objectid_check(['project_id'])
@params_required(['project_id'])
def all_interfaces():
    """
     1 获取所有任务,根据项目
    :return:
    """
    data = request.get_json()
    # data = json.loads(request.get_data().decode('utf-8'))
    page = 1
    page_size = 20
    project_id = data['project_id']

    if 'page' in data and 'page_size' in data:
        page = data['page']
        page_size = data['page_size']

    tasks = Task.objects(project=ObjectId(project_id))[page_size * (page - 1):page_size * page]
    total = Task.objects(project=ObjectId(project_id)).count()
    data = []
    for task in tasks:
        data.append(mongo_to_dict(task))
    info = {
        "total": total,
        "data": data
    }
    return init_return(info)


@blueprint.route('/<task_id>', methods=['GET', 'POST'])
def get_task(task_id):
    """
     2、根据id查看
    :param: task_id
    :return:
    """
    task = Task.objects(id=ObjectId(task_id))
    if task.count() == 0:
        return init_return({}, sucess=False, error="查找的任务不存在" % id, errorCode=1001)
    else:
        data = mongo_to_dict(task.first())
        return init_return(data)


@blueprint.route('/add', methods=['GET', 'POST'])
@project_check
@params_required(['project_id', 'name'])
def add():
    """
      3 新增任务接口
    :return:
    """
    data = request.get_json()
    task_use_cases = []
    name = data['name']
    project_id = data['project_id']

    existed = Task.objects(name=name, project=ObjectId(project_id)).first()
    if existed:
        return init_return({}, sucess=False, error="存在相同任务名", errorCode=1001)

    # if 'environment_id' in data and data['environment_id']!= '':
    #     environment_id = data['environment_id']
    #     environment = Environment.objects(id=ObjectId(environment_id)).first()
    #     if not environment:
    #         return init_return({}, sucess=False, error="任务选择的环境不存在", errorCode=1001)

    if 'use_cases' in data and len(data['use_cases'])!= 0:
        for use_case in data['use_cases']:
            use_case_id = use_case['id']
            use_case_name = use_case['name']
            use_case_request = use_case['request']

            for request_expect in use_case['expect']:
                params = request_expect['params']
                expect = request_expect['expect']
                rule = request_expect['rule']
                task_use_case = TaskUseCase(use_case_id=use_case_id, use_case_name=use_case_name,
                                            use_case_request=use_case_request, rule=rule,
                                            params=params, expect=expect, status=0)

                task_use_cases.append(task_use_case)

    environment = get_value(data, 'environment', {})
    description = get_value(data, 'description', '')

    summary = {
        'use_case_count': len(task_use_cases)
    }
    Task(name=name, project=ObjectId(project_id), environment=environment,
         use_cases=task_use_cases, status=0, summary=summary, remarks={'description': description}).save()
    return init_return({
        'data': '新增成功'
    })


@blueprint.route('/update', methods=['GET', 'POST'])
@params_empty_check(['name'])
@params_required(['id'])
def update():
    """
      4 根据任务id更新项目接口
      可更新数据 name, version, type, description
    :return:
    """
    data = request.get_json()
    id = data['id']
    name = data['name']

    task = Task.objects(id=ObjectId(id))
    if task.count() == 0:
        return init_return({}, sucess=False, error="更新的任务不存在", errorCode=1001)
    else:
        existed = Task.objects(name=name, project=task.first().project).first()
        if existed and str(existed.id) != id:
            return init_return({}, sucess=False, error="存在相同任务名", errorCode=1001)

        task_use_cases = []
        if 'use_cases' in data and len(data['use_cases']) != 0:
            for use_case in data['use_cases']:
                use_case_id = use_case['id']
                use_case_name = use_case['name']
                use_case_request = use_case['request']

                for request_expect in use_case['expect']:
                    params = request_expect['params']
                    expect = request_expect['expect']
                    rule = request_expect['rule']
                    task_use_case = TaskUseCase(use_case_id=use_case_id, use_case_name=use_case_name,
                                                use_case_request=use_case_request, rule=rule,
                                                params=params, expect=expect, status=0)

                    task_use_cases.append(task_use_case)

        environment = get_value(data, 'environment', {})
        description = get_value(data, 'description')

        source = mongo_to_dict(task.first())

        if name != source['name']:
            task.update_one(name=name)
        if environment != source['environment']:
            task.update_one(environment=environment)
        if task_use_cases != source['use_cases']:
            task.update_one(use_cases=task_use_cases)
        if description != source['remarks']['description']:
            task.update_one(remarks__description=description)

    return init_return({
        'data': '更新成功'
    })


@blueprint.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete(task_id):
    """
     5 根据任务id删除任务接口
    :param: project_id
    :return:
    """
    result = Task.objects(id=ObjectId(task_id)).delete()
    if result == 0:
        return init_return({}, sucess=False, error="删除的任务不存在", errorCode=1001)
    else:
        return init_return({'data':'删除成功'})

