# encoding: utf-8
"""
@author: han.li
@file  : s_interface_history.py
@time  : 11/15/18 2:56 PM
@dec   : 接口历史修改记录, 缓存最多5条记录
"""


from itest.model.m_interface_history import InterfaceHistory
from itest.service.user.s_user import UserService
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class InterfaceHistoryService(object):
    def __init__(self):
        pass

    @staticmethod
    def get(interface_id):
        status = 'ok'
        try:
            rs = InterfaceHistory.objects(interfaceId=ObjectId(interface_id)).first()
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    @staticmethod
    def push(interface):
        status = 'ok'
        try:
            operator_id = get_user_id()
            print(operator_id)
            name = UserService.get_by_id(operator_id)['name']
            record = {
                'data': interface,
                'operatorId': operator_id,
                'operatorName': name
            }
            print(record)
            history = InterfaceHistory.objects(interfaceId=ObjectId(interface['id']))
            if not history.first():
                rs = InterfaceHistory(records=[record],
                                      interfaceId=ObjectId(interface['id'])).save()
            else:
                if len(history.first().records) == 5:
                    InterfaceHistory.objects(interfaceId=ObjectId(interface['id'])).modify(
                        pop__records=-1)
                    rs = InterfaceHistory.objects(interfaceId=ObjectId(interface['id'])).modify(
                                 push__records=record,
                                 modifiedTime=datetime.utcnow,
                                 new=True)
                else:
                    rs = InterfaceHistory.objects(interfaceId=ObjectId(interface['id'])).modify(
                        push__records=record,
                        modifiedTime=datetime.utcnow,
                        new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status
