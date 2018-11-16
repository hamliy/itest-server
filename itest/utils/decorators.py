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


def model_handler(event):
    """mongo 信号装饰其."""

    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator


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
                return init_return({}, sucess=False, error="依赖的项目不存在", errorCode=1002)
            return func(*args, **kwargs)
        else:
            return init_return({}, sucess=False, error="请求参数需要使用json类型", errorCode=1003)
    return wrapper


def init_params(params, empty_check_params=[], empty_check=False):
    """输入参数初始化, 参数赋值， 参数不为空校验
        params: 参数输入检查
        empty_check: True 空检查等同params参数
        empty_check_params: 空检查参数列表
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 通过json请求
            if request.get_json() and request.get_json() is not None:
                data = request.get_json()

                init_items = []
                for param in params:
                    if param not in data:
                        init_items.append(param)
                if len(init_items) > 0:
                    return init_return({}, sucess=False, error="缺少参数%s" % ",".join(init_items), errorCode=1001)

                if empty_check:
                    empty_check_params.extend(params)

                empty_items = []
                for param in empty_check_params:
                    if param in data:
                        if type(data[param]).__name__ == 'str' and data[param].strip() == '':
                            empty_items.append(param)
                if len(empty_items) > 0:
                    return init_return({}, sucess=False, error="参数%s为不能为空" % ",".join(empty_items), errorCode=1002)
                return func(*args)
            else:
                return init_return({}, sucess=False, error="请求参数需要使用json类型", errorCode=1003)
        return wrapper

    return decorator
