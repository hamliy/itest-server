#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/11/18 下午5:06
# @Author  : lihan
# @File    : s_interface_use_case_group.py
# @Dec     : 



from itest.model.m_interface_use_case_group import InterfaceUseCaseGroup
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class InterfaceUseCaseGroupService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(interface_group):
        creator_id = get_user_id()
        return convert_mongo_to_json(InterfaceUseCaseGroup(name=interface_group['name'],
                                                    creatorId=ObjectId(creator_id),
                                                    projectId=ObjectId(interface_group['projectId']),
                                                    desc=interface_group['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(InterfaceUseCaseGroup.objects(name=name).first())

    @staticmethod
    def get_by_id(group_id):
        status = 'ok'
        try:
            rs = InterfaceUseCaseGroup.objects(id=ObjectId(group_id), isDeleted=False).first()
            if not rs:
                return None, 'not_find'
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    @staticmethod
    def get_groups(project_id):
        status = 'ok'
        try:
            rs = InterfaceUseCaseGroup.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
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
        return convert_queryset_to_json(InterfaceUseCaseGroup.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def add_member(group_id, use_case_id):
        InterfaceUseCaseGroup.objects(id=ObjectId(group_id), isDeleted=False)\
                .update_one(push__member=ObjectId(use_case_id))

    @staticmethod
    def delete_member(group_id, use_case_id):
        InterfaceUseCaseGroup.objects(id=ObjectId(group_id), isDeleted=False)\
                .update_one(pull__member=ObjectId(use_case_id))

    @staticmethod
    def update(interface_use_case_group):
        status = 'ok'
        try:
            data = InterfaceUseCaseGroup.objects(id=ObjectId(interface_use_case_group['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=interface_use_case_group['name'],
                             desc=interface_use_case_group['desc'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(interface_use_case_group_id):
        status = 'ok'
        try:
            data = InterfaceUseCaseGroup.objects(id=ObjectId(interface_use_case_group_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + interface_use_case_group_id
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status
