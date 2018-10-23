# encoding: utf-8
"""
@author: han.li
@file  : apis.py
@time  : 8/28/18 7:56 PM
@dec   : 
"""
from flask import Blueprint, request
import json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
"""
    用户相关接口
    用户相关：
    1 登录接口
    2 获取用户信息接口
    3 注销接口

"""
blueprint = Blueprint('user', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
     1 登录接口
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    username = data['username']
    password = data['password']
    if username != 'admin' or password != 'admin':
        return {
            "success": True,
            "errorCode": 201,
            "error": "用户名或密码错误",
            "data": {}
        }

    access_token = create_access_token(identity=username)
    return {
            "errorCode": 100,
            "success": True,
            "error": "",
            "data": {
                "token": access_token
            }
        }


@blueprint.route('/info', methods=['GET', 'POST'])
@jwt_required
def info():
    """
    2 获取用户信息接口
    :return:
    """
    user = get_jwt_identity()
    return {
            "errorCode": 100,
            "success": True,
            "error": "",
            "data": {
                "roles": [user],
                "name": user,
                "avatar": ''
            }
        }
