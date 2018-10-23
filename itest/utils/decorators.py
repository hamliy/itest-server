# encoding: utf-8
"""
@author: han.li
@file  : decorators.py
@time  : 9/6/18 3:33 PM
@dec   : 通用装饰器
"""
from bson import ObjectId
import json, os
from functools import wraps
from flask import request
from itest.utils.utils import init_return


def params_required(params):
    """必须参数校验"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.get_json() and request.get_json() is not None:
                data = request.get_json()
                items = []
                for param in params:
                    if param not in data or data[param] == '':
                        items.append(param)
                if len(items) > 0:
                    return init_return({}, sucess=False, error="请求参数%s为必填参数且不能为空" % ",".join(items), errorCode=1001)
                return func(*args)
            else:
                return init_return({}, sucess=False, error="请求参数需要使用json类型", errorCode=1001)
        return wrapper

    return decorator


def params_empty_check(params):
    """输入参数不为空校验"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.get_json() and request.get_json() is not None:
                data = request.get_json()
                items = []
                for param in params:
                    if param in data and data[param] == '':
                        items.append(param)
                if len(items) > 0:
                    return init_return({}, sucess=False, error="更新的参数%s为不能为空" % ",".join(items), errorCode=1001)
                return func(*args)
            else:
                return init_return({}, sucess=False, error="请求参数需要使用json类型", errorCode=1001)
        return wrapper

    return decorator


def params_objectid_check(params):
    """ObjectId字符串参数检验"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.get_json() and request.get_json() is not None:
                data = request.get_json()
                items = []
                for param in params:
                    if param in data and not ObjectId.is_valid(data[param]):
                        items.append(param)

                if len(items) > 0:
                    return init_return({}, sucess=False, error="请求参数%s值不为ObjectId，请确认" % ",".join(items), errorCode=1001)
                return func(*args)
            else:
                return init_return({}, sucess=False, error="请求参数需要使用json类型", errorCode=1001)
        return wrapper
    return decorator


def project_check(func):
    """项目是否存在校验"""
    from itest.models import Project

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.get_json() and request.get_json() is not None:
            data = request.get_json()
            if 'project_id' in data and data['project_id'] != '':
                project_id = data['project_id']
                project = Project.objects(id=ObjectId(project_id)).first()
                if not project:
                    return init_return({}, sucess=False, error="依赖的项目不存在", errorCode=1001)
            else:
                return init_return({}, sucess=False, error="依赖的项目不存在", errorCode=1001)
            return func(*args, **kwargs)
        else:
            return init_return({}, sucess=False, error="请求参数需要使用json类型", errorCode=1001)
    return wrapper
