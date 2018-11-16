# encoding: utf-8
"""
@author: han.li
@file  : a_interface_history.py
@time  : 11/15/18 5:04 PM
@dec   : 接口历史数据
"""

from flask import Blueprint, request
from itest.service.interface.s_interface_history import InterfaceHistoryService
from itest.utils.utils import init_return

blueprint = Blueprint('interface-history', __name__)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = InterfaceHistoryService.get(request.args.get('interfaceId'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="接口id不存在", errorCode=3003)
    return init_return(rs)

