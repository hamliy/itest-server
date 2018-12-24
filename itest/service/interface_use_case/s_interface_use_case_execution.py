#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/11/18 下午5:07
# @Author  : lihan
# @File    : s_interface_use_case_execution.py
# @Dec     : 用例执行


from itest.model.m_interface_use_case_execution import InterfaceUseCaseExecution
from itest.service.interface_use_case.s_interface_use_case_group import InterfaceUseCaseGroupService
from itest.service.interface_use_case.s_interface_use_case import InterfaceUseCaseService
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
        return convert_mongo_to_json(InterfaceUseCaseExecution(creatorId=ObjectId(creator_id),
                                                               useCaseId=ObjectId(use_case['id']),
                                                               relationId=ObjectId(use_case['relationId']),
                                                               executeType=use_case['executeType'],
                                                               useCaseName=use_case['name'],
                                                               useCaseDesc=use_case['desc'],
                                                               response={},
                                                               result={},
                                                               startTime=start_time).save())

    @staticmethod
    def create_execution_by_id(use_case_id):
        use_case = InterfaceUseCaseService.get_by_id(use_case_id)
        print(use_case)
        use_case['relationId'] = None
        use_case['executeType'] = 0
        return InterfaceUseCaseExecutionService.create_execution(use_case)

    @staticmethod
    def create_execution_by_group(group_id):
        start_time = datetime.utcnow
        creator_id = get_user_id()
        group, status = InterfaceUseCaseGroupService.get_by_id(group_id)
        use_case_list = InterfaceUseCaseService.get_by_id_list(group['member'])
        executions = []
        for use_case in use_case_list:
            execute = InterfaceUseCaseExecution(creatorId=ObjectId(creator_id),
                                                useCaseId=ObjectId(use_case['id']),
                                                relationId=ObjectId(group_id),
                                                executeType=1,
                                                useCaseNo=use_case['useCaseNo'],
                                                useCaseName=use_case['name'],
                                                useCaseDetail=use_case['detail'],
                                                response={},
                                                result={},
                                                startTime=start_time).save()
            executions.append(execute)

        return convert_queryset_to_json(executions)

    def create_execution_by_test_plan(test_plan_id):
        start_time = datetime.utcnow
        creator_id = get_user_id()
        group, status = InterfaceUseCaseGroupService.get_by_id(test_plan_id)
        use_case_list = InterfaceUseCaseService.get_by_id_list(group['member'])
        executions = []
        for use_case in use_case_list:
            execute = InterfaceUseCaseExecution(creatorId=ObjectId(creator_id),
                                                useCaseId=ObjectId(use_case['id']),
                                                relationId=ObjectId(test_plan_id),
                                                executeType=1,
                                                useCaseNo=use_case['useCaseNo'],
                                                useCaseName=use_case['name'],
                                                useCaseDetail=use_case['detail'],
                                                response={},
                                                result={},
                                                startTime=start_time).save()
            executions.append(execute)

        return convert_queryset_to_json(executions)

    @staticmethod
    def update_execution(execution_id, response, check_result):
        """
        更新执行结果
        :param execution_id:
        :param response:
        :param check_result:
        :return:
        """
        return convert_mongo_to_json(InterfaceUseCaseExecution.objects(id=ObjectId(execution_id)).modify(
            response=response,
            result=check_result,
            status=1,
            endTime=datetime.utcnow,
            new=True
        ))

    @staticmethod
    def get_by_id(use_case_id):
        return convert_mongo_to_json(InterfaceUseCaseExecution.objects(id=ObjectId(use_case_id), isDeleted=False).first())

    @staticmethod
    def get_by_project_id(project_id):
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
                             options=use_case['options'],
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