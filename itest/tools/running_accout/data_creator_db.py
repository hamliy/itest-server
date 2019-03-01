# encoding: utf-8
"""
@author: han.li
@file  : data_creator_db.py
@time  : 1/30/19 2:48 PM
@dec   : 模拟消息数据操作
"""
from pymongo import MongoClient
from datetime import datetime
import time
from itest.tools.running_accout.util import get_random_timestamp, time_stamp_to_str
import random
from urllib.parse import quote_plus



DATACREATOR_URI = "mongodb://%s:%s@%s" % (quote_plus('test'), quote_plus('HlCPj39gI3zu'), "123.207.7.95:31605")
DATACREATOR_DB = 'robert-data-creator-test'
DBSET = {
    'user': 'user_info', # 用户信息表
    'dispatch': 'dispatch_message', # 分发消息表 stage更新 endMsgId更新
    'stage': 'dispatch_stage',  # 分发阶段阶段 请求服务： 分发， 处理中： 锁定，  完成： 置为完成
    'message': 'message'    # 对话消息
}
REMARK = {
    'Dispatch': '分发',
    'Lock': '锁定',
    'Completed': '置为完成'
}


def get_set(dbset):
    """
    获取表
    :param dbset:
    :return:
    """
    md = MongoClient(DATACREATOR_URI)
    db = md[DATACREATOR_DB]
    return db[DBSET[dbset]]

def check_user_type(info):
    ds = get_set('user')
    msg = ds.find_one({'unionId': info['unionId']})
    if msg:
        return 0
    return 1

def insert_user(info):
    ds = get_set('user')
    data = {
        'timestamp': get_random_timestamp(),
        'unionId': info['unionId'],
        'yzjId': str(random.randint(100000, 1000000)),
        'createTime': get_random_timestamp(1),
        'enterpriseName': '金蝶研究院',
        'uName': info['userName'],
        'extensionInfo': '无',
        'role': '客户',
        '_class': 'com.example.demo.mode.userInfo'
    }
    result = ds.insert_one(data)
    if result.inserted_id:
        if '_id' in data:
            data.pop('_id')
        data['id'] = str(result.inserted_id)
        data['createTime'] = time_stamp_to_str(data['createTime'])
        return data
    else:
        return {}

def insert_message(message):
    ds = get_set('message')
    msg_id = (100000 + ds.count())
    if message['type'] == 'query':
        data = {
            'timestamp': get_random_timestamp(),
            'msgId': str(msg_id),
            'msgWxId': '66162%s' % msg_id,
            'createTime': message['createTime'],
            'userId': message['unionId'],
            'unionId': message['unionId'],
            'opUserId': '1',
            'fromUserId': message['unionId'],
            'fromUnionId': message['unionId'],
            'fromUserName': message['userName'],
            'toUserId': '1',
            'toUnionId': 'oWv-X1DUoK3K6rd7rwH0zILMxSeM',
            'toUserName': '徐少春',
            'msgType': 'text',
            'textContent': message['content'],
            '_class': 'com.example.demo.mode.Message'
        }
    else:
        data = {
            'timestamp': get_random_timestamp(),
            'msgId': str(msg_id),
            'msgWxId': '66162%s' % msg_id,
            'createTime': message['createTime'],
            'userId': message['unionId'],
            'unionId': message['unionId'],
            'opUserId': '1',
            'fromUserId': '1',
            'fromUnionId': 'oWv-X1DUoK3K6rd7rwH0zILMxSeM',
            'fromUserName': '徐少春',
            'toUserId': message['unionId'],
            'toUnionId': message['unionId'],
            'toUserName': message['userName'],
            'msgType': 'text',
            'textContent': message['content'],
            '_class': 'com.example.demo.mode.Message'
        }
    result = ds.insert_one(data)
    if result.inserted_id:
        if '_id' in data:
            data.pop('_id')
        data['id'] = str(result.inserted_id)
        data['createTime'] = time_stamp_to_str(data['createTime'])
        return data
    else:
        return {}


def check_message_type(msg_id):
    ds = get_set('message')
    msg = ds.find_one({'msgId': msg_id})
    if msg:
        if msg['fromUnionId'] == 'oWv-X1DUoK3K6rd7rwH0zILMxSeM':
            return 2
        return 0
    return 1

def check_already_dispatch(msg_id):
    ds = get_set('dispatch')
    dp = ds.find_one({'beginMsgId':msg_id})
    if dp:
        return True
    else:
        return False

def insert_dispatch_message(info):
    ds = get_set('dispatch')
    dispatch_id = (100000 + ds.count())
    dispatch_stage_id = (1000 + ds.count())
    data = {
        'timesTamp': get_random_timestamp(),
        'unionId': info['unionId'],
        'dispatchStageId': dispatch_stage_id,
        'dispatchId': str(dispatch_id),
        'beginMsgId': str(info['msgId']),
        'endMsgId': str(info['msgId']),
        'createTime': info['createTime'],
        'modifiedTime': info['createTime'],
        '_class': 'com.example.demo.model.DispatchMessage',
    }
    result = ds.insert_one(data)
    if result.inserted_id:
        if '_id' in data:
            data.pop('_id')
        data['id'] = str(result.inserted_id)
        data['createTime'] = time_stamp_to_str(data['createTime'])
        return data
    else:
        return {}

def get_all_message(info):
    ds = get_set('message')
    all = ds.find({'unionId': info['unionId']})
    result = []
    for one in all:
        result.append({
            'id': str(one['_id']),
            'msgId': one['msgId'],
            'fromUserName': one['fromUserName'],
            'toUserName': one['fromUserName'],
            'unionId': one['unionId'],
            'createTime': time_stamp_to_str(one['createTime']),
            'textContent': one['textContent']
        })
    return result


def modify_message_time(info):
    ds = get_set('message')
    msg = ds.find_one({'unionId': info['unionId'],'msgId':info['msgId']})
    if msg:
        result = ds.update_one({'unionId': info['unionId'],'msgId':info['msgId']},
                               {'createTime': info['createTime']})
        if result.upserted_id:
            if '_id' in msg:
                data.pop('_id')
            data['id'] = str(result.upserted_id)
            data['createTime'] = time_stamp_to_str(data['createTime'])
            return data
        else:
            return {}


def update_dispatch_message(info):
    ds = get_set('dispatch')
    dispatch_id = (100000 + ds.count())
    data = {
        'timestamp': get_random_timestamp(),
        'dispatchId': str(dispatch_id),
        'beginMsgId': str(info['msgId']),
        'endMsgId': str(info['msgId']),
        'createTime': info['createTime'],
        'modifiedTime': info['createTime'],
        '_class': 'com.example.demo.model.DispatchMessage',
    }
    result = ds.update_one({'dispatchId': info['dispatchId']},
                  {'modifiedTime': info['createTime'],
                   'endMsgId': info['msgId']})
    if result.upserted_id:
        if '_id' in data:
            data.pop('_id')
        data['id'] = str(result.upserted_id)
        data['createTime'] = time_stamp_to_str(data['createTime'])
        return data
    else:
        return {}

def check_stage_type(info):
    ds = get_set('stage')
    stage = info['stage']
    has_dispatch = ds.find_one({'dispatchId': info['dispatchId']})
    if not has_dispatch:
        return 3
    if stage == 'Lock':
        return 0
    else:
        has_lock = ds.find_one({'dispatchId': info['dispatchId'],'dispatchType':'Lock'})
        has_completed = ds.find_one({'dispatchId': info['dispatchId'], 'dispatchType': 'Completed'})
        if not has_lock:
            return 1
        elif has_completed:
            return 2
        else:
            return 0

def insert_stage(info):
    ds = get_set('stage')
    data = {
        'timestamp': get_random_timestamp(),
        'dispatchId': str(info['dispatchId']),
        'unionId': str(info['unionId']),
        'createTime': info['createTime'],
        'fromUserId': '1',
        'fromUserName': '徐少春',
        'toUserId': '2',
        'toUserName': '李宏武',
        'dispatchType': info['stage'],
        'remark': REMARK[info['stage']],
        '_class': 'com.example.demo.model.DispatchStage',
    }
    result = ds.insert_one(data)
    if result.inserted_id:
        if '_id' in data:
            data.pop('_id')
        data['id'] = str(result.inserted_id)
        data['createTime'] = time_stamp_to_str(data['createTime'])
        return data
    else:
        return {}

def is_time_stage_wrong(time):
    ds = get_set('stage')


if __name__ == '__main__':
    ds = get_set('message')
    print(ds.count())
    # user = {
    #     'userName': '李涵',
    #     'unionId': 'owv-x1ktxpfery2mkedddddd'
    # }
    # insert_user(user['userName'], user['unionId'])
    # unionId = ''
    # userName = ''
    # content = ''
    # m_type = 'query'
    # stage = 'Dispatch'
    # message = {
    #     'type': m_type,
    #     'createTime': get_random_timestamp(100),
    #     'userName': userName,
    #     'unionId': unionId,
    #     'content': content
    # }
    # msg_id = insert_message(message)
    # info = {}
    # if msg_id and stage == 'Dispatch':
    #     insert_dispatch(info).limit(1)

    data = ds.find({'userId': '1000'}).sort([
                    ('createTime', 1)]).limit(1)
    for i in data:
        print(i)
