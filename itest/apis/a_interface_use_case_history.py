# encoding: utf-8
"""
@author: han.li
@file  : a_interface_use_case_history.py
@time  : 11/20/18 3:14 PM
@dec   : 接口用例修改历史
"""

from flask import Blueprint, request
from itest.service.interface_use_case.s_interface_use_case_history import InterfaceUseCaseHistoryService
from itest.utils.utils import init_return

blueprint = Blueprint('interface-use-case-history', __name__)


@blueprint.route('/get', methods=['GET', 'POST'])
def get():
    rs, status = InterfaceUseCaseHistoryService.get(request.args.get('useCaseId'))
    if status == 'not_object_id':
        return init_return({}, sucess=False, error="用例id不存在", errorCode=3003)
    return init_return(rs)