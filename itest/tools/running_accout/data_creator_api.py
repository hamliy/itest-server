# encoding: utf-8
"""
@author: han.li
@file  : data_creator_api.py
@time  : 1/30/19 8:39 PM
@dec   : 
"""


from flask import Blueprint, request
from itest.utils.utils import init_return
from itest.utils.decorators import init_params
from itest.tools.running_accout.data_creator_db import insert_message, \
    insert_stage, insert_dispatch_message, check_message_type, check_stage_type,check_already_dispatch,\
    insert_user,check_user_type,get_all_message
from itest.tools.running_accout.util import time_str_to_stamp, time_stamp_to_str

blueprint = Blueprint('runningAccount', __name__)


@blueprint.route('/ask_message', methods=['POST'])
@init_params(params=['unionId', 'createTime', 'userName', 'content'])
def ask_message():
    info = request.get_json()
    info['type'] = 'query'
    info['createTime'] = time_str_to_stamp(info['createTime'])
    data = insert_message(info)
    if data:
        return init_return(data)
    else:
        return init_return(data, sucess=False, errorCode=400, error='插入消息失败')


@blueprint.route('/answer_message', methods=['POST'])
@init_params(params=['unionId', 'createTime', 'userName', 'content'])
def answer_message():
    info = request.get_json()
    info['type'] = 'answer'
    info['createTime'] = time_str_to_stamp(info['createTime'])
    data = insert_message(info)
    if data:
        return init_return(data)
    else:
        return init_return(data, sucess=False, errorCode=400, error='插入消息失败')


@blueprint.route('/dispatch_message', methods=['POST'])
@init_params(params=['createTime', 'msgId', 'unionId'])
def dispatch_message():
    info = request.get_json()
    info['createTime'] = time_str_to_stamp(info['createTime'])
    msg_type = check_message_type(info['msgId'])
    if msg_type == 0:
        if check_already_dispatch(info['msgId']):
            return init_return({}, sucess=False, errorCode=400, error='该消息已被分配过')
        dm_info = insert_dispatch_message(info)
        if not dm_info:
            return init_return({}, sucess=False, errorCode=400, error='插入消息失败')
        info['dispatchId'] = dm_info['dispatchId']
        info['stage'] = 'Dispatch'
        data = insert_stage(info)
        if data:
            return init_return({'dispatchMsg': dm_info, 'dispatchStage': data})
        else:
            return init_return({}, sucess=False, errorCode=400, error='设置阶段失败失败')
    elif msg_type == 1:
        return init_return({}, sucess=False, errorCode=400, error='查找不到该msgId')
    elif msg_type == 2:
        return init_return({}, sucess=False, errorCode=400, error='请选择提问人的msgId')


@blueprint.route('/set_stage', methods=['POST'])
@init_params(params=['dispatchId', 'createTime', 'stage', 'unionId'])
def set_stage():
    info = request.get_json()
    info['createTime'] = time_str_to_stamp(info['createTime'])

    if info['stage'] not in ['处理中', '完成']:
        return init_return({}, sucess=False, errorCode=400, error='stage 参数只能为 处理中或完成')
    else:
        if info['stage'] == '处理中':
            info['stage'] = 'Lock'
        if info['stage'] == '完成':
            info['stage'] = 'Completed'
        stage_type = check_stage_type(info)
        if stage_type == 0:
            data = insert_stage(info)
            if data:
                return init_return(data)
            else:
                return init_return({}, sucess=False, errorCode=400, error='设置流程失败')
        elif stage_type == 1:
            return init_return({}, sucess=False, errorCode=400, error='问题未进行处理，请先处理再设置为完成')
        elif stage_type == 2:
            return init_return({}, sucess=False, errorCode=400, error='该服务单已为完成，请务重复设置完成')
        elif stage_type == 3:
            return init_return({}, sucess=False, errorCode=400, error='dispatchId未找到数据')


@blueprint.route('/create_user', methods=['POST'])
@init_params(params=['userName', 'unionId'])
def create_user():
    info = request.get_json()
    if check_user_type(info) == 0:
        return init_return({}, sucess=False, errorCode=400, error='用户unionId已存在')
    data = insert_user(info)
    if data:
        return init_return(data)
    else:
        return init_return({}, sucess=False, errorCode=400, error='新增用户失败失败')


@blueprint.route('/all_message', methods=['POST'])
@init_params(params=['unionId'])
def all_message():
    info = request.get_json()
    data = get_all_message(info)
    if data:
        return init_return(data)
    else:
        return init_return({}, sucess=False, errorCode=400, error='查询失败失败')

@blueprint.route('/modify_time', methods=['POST'])
@init_params(params=['unionId','msgId','createTime'])
def all_message():
    info = request.get_json()
    data = get_all_message(info)
    if data:
        return init_return(data)
    else:
        return init_return({}, sucess=False, errorCode=400, error='查询失败失败')
