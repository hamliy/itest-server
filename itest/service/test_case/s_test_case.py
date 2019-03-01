# encoding: utf-8
"""
@author: han.li
@file  : s_test_case.py
@time  : 2/28/19 4:27 PM
@dec   : 测试用例服务
"""

from itest.model.m_test_case import TestCase
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class TestCaseService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(use_case):
        creator_id = get_user_id()
        return convert_mongo_to_json(TestCase(name=use_case['name'],
                                              configType=use_case['configType'],
                                              belongProjectId=use_case['projectId'],
                                              belongModuleId=use_case['moduleId'],
                                              include=use_case['include'],
                                              level=use_case['level'],
                                              request=use_case['request'],
                                              creatorId=ObjectId(creator_id),
                                              desc=use_case['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(TestCase.objects(name=name).first())

    @staticmethod
    def get_by_id(project_id):
        return convert_mongo_to_json(TestCase.objects(id=ObjectId(project_id)).first())

    @staticmethod
    def get_projects():
        total = TestCase.objects().count()
        data = convert_queryset_to_json(TestCase.objects(isDeleted=False).order_by("-createTime"))
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
        total = TestCase.objects().count()
        data = convert_queryset_to_json(TestCase.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False)).order_by("-createTime")
                                        [page_size * (page - 1):page_size * page])
        return {
            "total": total,
            "data": data
        }

    @staticmethod
    def update(use_case):
        status = 'ok'
        try:
            data = TestCase.objects(id=ObjectId(use_case['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=use_case['name'],
                             configType=use_case['configType'],
                             belongProjectId=use_case['projectId'],
                             belongModuleId=use_case['moduleId'],
                             include=use_case['include'],
                             level=use_case['level'],
                             request=use_case['request'],
                             desc=use_case['desc'],
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
    def delete(use_case_id):
        status = 'ok'
        try:
            data = TestCase.objects(id=ObjectId(use_case_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + use_case_id
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
