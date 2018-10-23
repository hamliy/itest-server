#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/9/2 下午7:15
# @Author  : lihan
# @File    : environment_api.py
# @Dec     : 

"""
    环境基本功能api：
    1、查看全部
    2、根据id查看
    3、新增
    4、修改
    5、删除
"""

from flask import Blueprint, request
from itest.models import Environment, Project
from bson import ObjectId
from itest.utils.utils import init_return, mongo_to_dict, get_value
from itest.utils.decorators import params_required, params_objectid_check, project_check, params_empty_check
import json

blueprint = Blueprint('environment', __name__)


@blueprint.route('/all', methods=['POST'])
@params_objectid_check(['project_id'])
@params_required(['project_id'])
def all_environment():
    """
     1 获取所有接口信息接口,根据项目
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

    environments = Environment.objects(project=ObjectId(project_id))[page_size * (page - 1):page_size * page]
    total = Environment.objects(project=ObjectId(project_id)).count()
    data = []
    for environment in environments:
        data.append(mongo_to_dict(environment))
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)


# @blueprint.route('/<environment_id>', methods=['GET', 'POST'])
# def get_environment(environment_id):
#     """
#      2、根据id查看
#     :param: environment_id
#     :return:
#     """
#     environment = Environment.objects(id=ObjectId(environment_id))
#     if environment.count() == 0:
#         return init_return({}, sucess=False, error="查找的环境不存在" % id, errorCode=1001)
#     else:
#         return init_return(mongo_to_dict(environment.first()))


@blueprint.route('/create', methods=['GET', 'POST'])
@project_check
@params_required(['project_id', 'name', 'value', 'type'])
def add():
    """
      3 新增环境接口
    :return:
    """
    data = request.get_json()
    name = data['name']
    value = data['value']
    type = data['type']
    project_id = data['project_id']

    existed = Environment.objects(name=name, project=ObjectId(project_id)).first()
    if existed:
        return init_return({}, sucess=False, error="存在相同环境名", errorCode=1001)

    description = get_value(data, 'description', '')

    Environment(name=name, project=ObjectId(project_id), value=value, type=type, description=description).save()
    return init_return({
        'data': '新增成功'
    })


@blueprint.route('/update', methods=['GET', 'POST'])
@params_empty_check(['name', 'value'])
@params_required(['id'])
def update():
    """
      4 根据环境id更新项目接口
      可更新数据 name, url,  description
    :return:
    """
    data = request.get_json()
    id = data['id']
    name = data['name']
    value = data['value']

    environment = Environment.objects(id=ObjectId(id))
    if environment.count() == 0:
        return init_return({}, sucess=False, error="更新的环境不存在", errorCode=1001)
    else:
        existed = Environment.objects(name=name, project=environment.first().project).first()
        if existed and str(existed.id) != id:
            return init_return({}, sucess=False, error="存在相同名称", errorCode=1001)

        description = get_value(data, 'description')

        source = mongo_to_dict(environment.first())

        if name != source['name']:
            environment.update_one(name=name)
        if value != source['value']:
            environment.update_one(value=value)
        if description != source['description']:
            environment.update_one(description=description)

        return init_return({
            'data': '更新成功'
        })


@blueprint.route('/delete/<environment_id>', methods=['GET', 'POST'])
def delete(environment_id):
    """
     5 根据项目id删除项目接口
    :param: project_id
    :return:
    """
    result = Environment.objects(id=ObjectId(environment_id)).delete()
    if result == 0:
        return init_return({}, sucess=False, error="删除的环境不存在", errorCode=1001)
    else:
        return init_return({'data': '删除成功'})

