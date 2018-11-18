#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/11/18 下午5:07
# @Author  : lihan
# @File    : s_interface_use_case_history.py
# @Dec     : 用例修改历史


from itest.model.m_interface_use_case_history import InterfaceUseCaseHistory
from itest.service.user.s_user import UserService
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class InterfaceUseCaseHistoryService(object):
    def __init__(self):
        pass

    @staticmethod
    def get(interface_id):
        status = 'ok'
        try:
            rs = InterfaceUseCaseHistory.objects(interfaceId=ObjectId(interface_id)).first()
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    @staticmethod
    def push(use_case):
        status = 'ok'
        try:
            operator_id = get_user_id()
            print(operator_id)
            name = UserService.get_by_id(operator_id)['name']
            record = {
                'data': use_case ,
                'operatorId': operator_id,
                'operatorName': name
            }
            history = InterfaceUseCaseHistory.objects(useCaseId=ObjectId(use_case['id']))
            if not history.first():
                rs = InterfaceUseCaseHistory(records=[record],
                                      useCaseId=ObjectId(use_case['id'])).save()
            else:
                if len(history.first().records) == 5:
                    InterfaceUseCaseHistory.objects(useCaseId=ObjectId(use_case['id'])).modify(
                        pop__records=-1)
                    rs = InterfaceUseCaseHistory.objects(useCaseId=ObjectId(use_case['id'])).modify(
                                 push__records=record,
                                 modifiedTime=datetime.utcnow,
                                 new=True)
                else:
                    rs = InterfaceUseCaseHistory.objects(useCaseId=ObjectId(use_case['id'])).modify(
                        push__records=record,
                        modifiedTime=datetime.utcnow,
                        new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status