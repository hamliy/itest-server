#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/9/2 下午7:15
# @Author  : lihan
# @File    : project_api.py
# @Dec     : 

"""
    项目基本功能api：
    1、查看全部
    2、根据id查看
    3、新增
    4、修改
    5、删除
"""

from flask import Blueprint, request
from itest.models import Project
from bson import ObjectId
from itest.utils.utils import init_return, get_value, mongo_to_dict, convert_mongo_to_json
from itest.utils.decorators import params_required, params_objectid_check, project_check

blueprint = Blueprint('project', __name__)


@blueprint.route('/all', methods=['GET', 'POST'])
def all_projects():
    """
     1 获取所有项目信息接口
    :return:
    """
    data = request.get_json()
    page = 1
    page_size = 20
    if data and data is not None:
        if 'page' in data and 'page_size' in data:
            page = data['page']
            page_size = data['page_size']

    projects = Project.objects()[page_size * (page - 1):page_size * page]
    total = Project.objects().count()
    data = []
    for project in projects:
        data.append(convert_mongo_to_json(project))
        # print(convert_mongo_to_json(project))
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)


@blueprint.route('/query', methods=['GET', 'POST'])
def query_projects():
    """
     1 查询项目
    :return:
    """
    data = request.get_json()
    print(data)
    page_size = 20
    page = 1
    query_name = ''
    if data and data is not None:
        if 'page' in data and 'page_size' in data:
            page = data['page']
            page_size = data['page_size']
        if 'query_name' in data:
            query_name = data['query_name']

    projects = Project.objects(name__icontains=query_name)[page_size * (page - 1):page_size * page]
    total = Project.objects().count()
    data = []
    for project in projects:
        data.append(mongo_to_dict(project))
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)


@blueprint.route('/<project_id>', methods=['GET', 'POST'])
def get_project(project_id):
    """
     2、根据id查看
    :param: project_id
    :return:
    """
    project = Project.objects(id=ObjectId(project_id))
    if project.count() == 0:
        return init_return({}, sucess=False, error="查找的项目不存在" % id, errorCode=1001)
    else:
        data = project.first().to_dict()
        return init_return(data)


@blueprint.route('/create', methods=['GET', 'POST'])
@params_required(['name'])
def add():
    """
      3 新增项目接口
    :return:
    """
    data = request.get_json()
    name = data['name']

    projects = Project.objects(name=data['name'])
    if projects.count() != 0:
        return init_return({}, sucess=False, error="存在相同项目名" , errorCode=1001)

    version = get_value(data, 'version', '')
    type = get_value(data, 'type', 'web')
    description = get_value(data, 'description', '')

    Project(name=name, version=version, type=type, description=description).save()
    return init_return({
        'data': '新增成功'
    })


@blueprint.route('/update', methods=['GET', 'POST'])
@params_required(['id','name'])
def update():
    """
      4 根据项目project_id更新项目接口
      可更新数据 name, version, type, description
    :return:
    """
    data = request.get_json()
    id = data['id']
    name = data['name']

    project = Project.objects(id=ObjectId(id))
    if project.count() == 0:
        return init_return({}, sucess=False, error="更新的项目不存在", errorCode=1001)
    else:
        existed = Project.objects(name=name).first()
        if existed and str(existed.id) != id:
            return init_return({}, sucess=False, error="存在相同项目名", errorCode=1001)

        version = get_value(data, 'version')
        type = get_value(data, 'type', 'get')
        description = get_value(data, 'description')
        print(data)
        source = mongo_to_dict(project.first())
        print(source)
        if name != source['name']:
            project.update_one(name=name)
        if version != source['version']:
            project.update_one(version=version)
        if type != source['type']:
            project.update_one(type=type)
        if description != source['description']:
            project.update_one(description=description)

        return init_return({
            'data': '更新成功'
        })


@blueprint.route('/delete', methods=['GET', 'POST'])
def delete():
    """
     5 根据项目id删除项目接口
    :param: project_id
    :return:
    """
    data = request.get_json()
    project_id = data['id']
    result = Project.objects(id=ObjectId(project_id)).delete()
    if result == 0:
        return init_return({}, sucess=False, error="删除的项目不存在", errorCode=1001)
    else:
        return init_return({'data': '删除成功'})


