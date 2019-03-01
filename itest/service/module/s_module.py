# encoding: utf-8
"""
@author: han.li
@file  : module.py
@time  : 2/28/19 3:59 PM
@dec   : 模块服务
"""

from itest.model.m_module import Module
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class ModuleService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(module):
        creator_id = get_user_id()
        return convert_mongo_to_json(Module(name=module['name'],
                                            testUser=module['testUser'],
                                            belongProjectId=ObjectId(module['projectId']),
                                            creatorId=ObjectId(creator_id),
                                            desc=module['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(Module.objects(name=name).first())

    @staticmethod
    def get_by_id(project_id):
        return convert_mongo_to_json(Module.objects(id=ObjectId(project_id)).first())

    @staticmethod
    def get_modules():
        total = Module.objects().count()
        data = convert_queryset_to_json(Module.objects(isDeleted=False).order_by("-createTime"))
        return {
            "total": total,
            "data": data
        }

    @staticmethod
    def find(q, page=1, page_size=10):
        """
        模糊查询
        :return:
        """
        total = Module.objects().count()
        data = convert_queryset_to_json(Module.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False)).order_by("-createTime")
                                        [page_size * (page - 1):page_size * page])
        return {
            "total": total,
            "data": data
        }

    @staticmethod
    def update(module):
        status = 'ok'
        try:
            data = Module.objects(id=ObjectId(module['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=module['name'],
                             testUser=module['testUser'],
                             desc=module['desc'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except NotUniqueError:
            rs = None
            status = 'not_unique'
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(module_id):
        status = 'ok'
        try:
            data = Module.objects(id=ObjectId(module_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + project_id
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except NotUniqueError:
            rs = None
            status = 'not_unique'
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status
