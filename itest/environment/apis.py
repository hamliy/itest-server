# encoding: utf-8
"""
@author: han.li
@file  : apis.py
@time  : 8/15/18 4:29 PM
@dec   : 环境相关接口
"""
from flask import Blueprint

blueprint = Blueprint('env', __name__)


@blueprint.route('/details', methods=['GET'])
def get_env_details():
    """
    环境信息列表
    :return:
    """
    return {
            "errorCode": 0,
            "description": "Success",
            "data": ""
        }
