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
        if interface['options'] == {}:
            interface['options'] = InterfaceService.get_interface_default_option()
        return convert_mongo_to_json(Interface(name=interface['name'],
                                               method=interface['method'],
                                               path=interface['path'],
                                               options=interface['options'],
                                               creatorId=ObjectId(creator_id),
                                               projectId=ObjectId(interface['projectId']),
                                               groupId=ObjectId(interface['groupId']),
                                               desc=interface['desc']).save())

    @staticmethod
    def get_interface_default_option():
        """
        获取莫接口配置
        :return:
        """
        return {
            "headers":{
                "params": [{
                    'key': 'Content-Type',
                    'example': 'application/json',
                    'required': True,
                    'type': 'string',
                    'comment': '默认json请求'
                }],
                "example": {}
            },
            "params": {
                "body": [],
                "path": [],
                "query": []
            },
            "examples": {
                "body": {},
                "path": {},
                "query": {}
            },
            "response": [
                {
                    "status": 200,
                    "statusText": '请求成功',
                    "params": [{
                        'comment': None,
                        'required': True,
                        'type': "string",
                        'key': None
                    }],
                    "example": {}
                }
            ]
        }

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(Interface.objects(name=name).first())

    @staticmethod
    def get_by_id(_id):
        return convert_mongo_to_json(Interface.objects(id=ObjectId(_id), isDeleted=False).first())

    @staticmethod
    def get_by_group_id(group_id):
        return convert_queryset_to_json(Interface.objects(groupId=ObjectId(group_id), isDeleted=False))

    @staticmethod
    def get_group_interface(project_id):
        groups, status = InterfaceGroupService.get_groups(project_id)
        # tree = []
        # # 循环所有接口 按组分组 生成树结构
        # for group in groups:
        #     tree.append({
        #         'name': group['name'],
        #         'id': group['id'],
        #         'member': group['member']
        #     })
        return groups

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
                             options=interface['options'],
                             desc=interface['desc'],
                             path=interface['path'],
                             method=interface['method'],
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
