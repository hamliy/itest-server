#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/11/18 下午5:07
# @Author  : lihan
# @File    : s_interface_use_case_execution.py
# @Dec     : 用例执行



from itest.service.interface_use_case.s_interface_use_case import InterfaceUseCaseService
from itest.model.m_interface_use_case_execution import InterfaceUseCaseExecution
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class InterfaceUseCaseExecutionService(object):
    def __init__(self):
        pass

    @staticmethod
    def create_execution(use_case):
        start_time = datetime.utcnow
        creator_id = get_user_id()
        return convert_mongo_to_json(InterfaceUseCaseExecution(name=use_case['name'],
                                                               creatorId=ObjectId(creator_id),
                                                               useCaseId=ObjectId(use_case['id']),
                                                               useCaseNo=use_case['useCaseNo'],
                                                               useCaseName=use_case['name'],
                                                               useCaseDetail=use_case['detail'],
                                                               response={},
                                                               result={},
                                                               startTime=start_time).save())

    @staticmethod
    def update_execution(execution_id, response, check_result):
        return convert_mongo_to_json(InterfaceUseCaseExecution.objects(id=ObjectId(execution_id)).modify(
            response=response,
            result=check_result,
            status=1,
            endTime=datetime.utcnow
        ))
    @staticmethod
    def execute_by_id(use_case_id):
        use_case = InterfaceUseCaseService.get_by_id(use_case_id)
        execution = InterfaceUseCaseExecutionService.create_execution(use_case_id)
        response, check_result = InterfaceUseCaseService.execute_use_case(use_case)
        return convert_mongo_to_json(InterfaceUseCaseExecution.objects())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(InterfaceUseCaseExecution.objects(name=name).first())

    @staticmethod
    def get_by_id(use_case_id):
        return convert_mongo_to_json(InterfaceUseCaseExecution.objects(id=ObjectId(use_case_id), isDeleted=False).first())

    @staticmethod
    def get_UseCases(project_id):
        status = 'ok'
        try:
            rs = InterfaceUseCaseExecution.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_queryset_to_json(rs), status

    @staticmethod
    def find(q, project_id):
        """
        模糊查询
        :return:
        """
        return convert_queryset_to_json(InterfaceUseCaseExecution.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def update(use_case):
        status = 'ok'
        try:
            data = InterfaceUseCaseExecution.objects(id=ObjectId(use_case['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=use_case['name'],
                             desc=use_case['desc'],
                             interfaceId=ObjectId(use_case['projectId']),
                             environmentId=ObjectId(use_case['environmentId']),
                             groupId=ObjectId(use_case['groupId']),
                             level=use_case['level'],
                             useCaseNo=use_case['useCaseNo'],
                             detail=use_case['detail'],
                             option=use_case['option'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        except NotUniqueError:
            rs = None
            status = 'not_unique'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(use_case):
        status = 'ok'
        try:
            data = InterfaceUseCaseExecution.objects(id=ObjectId(use_case), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + use_case
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status