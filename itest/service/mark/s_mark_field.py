# encoding: utf-8
"""
@author: han.li
@file  : s_mark_field.py
@time  : 11/5/18 2:04 PM
@dec   : 标签信息类
"""


from itest.model.m_mark_field import MarkField
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class MarkFieldService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(mark_field):
        return convert_mongo_to_json(MarkField(name=mark_field['name'],
                                               project_id=ObjectId(mark_field['projectId']),
                                               fieldType=mark_field['fieldType'],
                                               fieldItems=mark_field['fieldItems'],
                                               desc=mark_field['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(MarkField.objects(name=name).first())

    @staticmethod
    def get_by_id(mark_field_id):
        return convert_mongo_to_json(MarkField.objects(id=ObjectId(mark_field_id), isDeleted=False).first())

    @staticmethod
    def get_marks(project_id):
        status = 'ok'
        try:
            rs = MarkField.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
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
        return convert_queryset_to_json(MarkField.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def update(mark_field):
        status = 'ok'
        try:
            data = MarkField.objects(id=ObjectId(mark_field['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=mark_field['name'],
                             desc=mark_field['desc'],
                             fieldType=mark_field['fieldType'],
                             fieldItems=mark_field['fieldItems'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(mark_field_id):
        status = 'ok'
        try:
            data = MarkField.objects(id=ObjectId(mark_field_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + image_group_id
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

