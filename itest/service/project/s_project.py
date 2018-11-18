# encoding: utf-8
"""
@author: han.li
@file  : s_project.py
@time  : 11/6/18 3:14 PM
@dec   : 项目服务
"""
from itest.model.m_project import Project
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class ProjectService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(project):
        creator_id = get_user_id()
        return convert_mongo_to_json(Project(name=project['name'],
                                             projectType=project['projectType'],
                                             creatorId=ObjectId(creator_id),
                                             desc=project['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(Project.objects(name=name).first())

    @staticmethod
    def get_by_id(project_id):
        return convert_mongo_to_json(Project.objects(id=ObjectId(project_id)).first())

    @staticmethod
    def get_projects():
        return convert_queryset_to_json(Project.objects(isDeleted=False).order_by("-createTime"))

    @staticmethod
    def find(q):
        """
        模糊查询
        :return:
        """
        return convert_queryset_to_json(Project.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False)).order_by("-createTime"))

    @staticmethod
    def update(project):
        status = 'ok'
        try:
            data = Project.objects(id=ObjectId(project['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=project['name'],
                             projectType=project['projectType'],
                             desc=project['desc'],
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
    def delete(project_id):
        status = 'ok'
        try:
            data = Project.objects(id=ObjectId(project_id), isDeleted=False)
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

