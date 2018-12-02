# encoding: utf-8
"""
@author: han.li
@file  : s_interface.py
@time  : 11/5/18 2:03 PM
@dec   : 接口处理类
"""



from itest.model.m_interface import Interface
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from itest.service.interface.s_interface_group import InterfaceGroupService
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class InterfaceService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(interface):
        creator_id = get_user_id()
        return convert_mongo_to_json(Interface(name=interface['name'],
                                               method=interface['method'],
                                               path=interface['path'],
                                               option=interface['option'],
                                               creatorId=ObjectId(creator_id),
                                               projectId=ObjectId(interface['projectId']),
                                               groupId=ObjectId(interface['groupId']),
                                               desc=interface['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(Interface.objects(name=name).first())

    @staticmethod
    def get_by_id(_id):
        return convert_mongo_to_json(Interface.objects(id=ObjectId(_id), isDeleted=False).first())

    @staticmethod
    def get_by_group_id(group_id):
        return convert_mongo_to_json(Interface.objects(id=ObjectId(group_id), isDeleted=False).first())
    @staticmethod
    def get_order_by_group(project_id):
        interfaces = convert_queryset_to_json(Interface.objects(projectId=ObjectId(project_id), isDeleted=False))
        tree = []
        # 循环所有接口 按组分组 生成树结构
        for interface in interfaces:
            has_group = False
            # 判断是否已存在组
            for group in tree:
                if interface['groupId'] == group['id']:
                    group['member'].push({
                        'name': interface['name'],
                        'id': interface['id']
                    })
                    has_group = True
            # 如果不存在 则新增
            if not has_group:
                # 获取组名
                group_name = InterfaceGroupService.get_by_id(interface['groupId'])
                tree.append({
                    'id': interface['groupId'],
                    'name': group_name,
                    'member': [{
                        'name': interface['name'],
                        'id': interface['id']
                    }]
                })
        return tree

    @staticmethod
    def get_interfaces(project_id):
        status = 'ok'
        try:
            rs = Interface.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
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
        return convert_queryset_to_json(Interface.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def update(interface):
        status = 'ok'
        try:
            data = Interface.objects(id=ObjectId(interface['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=interface['name'],
                             option=interface['option'],
                             desc=interface['desc'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(interface_id):
        status = 'ok'
        try:
            data = Interface.objects(id=ObjectId(interface_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + interface_id
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status
