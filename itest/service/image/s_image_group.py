# encoding: utf-8
"""
@author: han.li
@file  : s_image_group.py
@time  : 11/14/18 3:02 PM
@dec   : 图片分组
"""


from itest.model.m_image_group import ImageGroup
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id


class ImageGroupService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(image_group):
        creator_id = get_user_id()
        return convert_mongo_to_json(ImageGroup(name=image_group['name'],
                                                creatorId=ObjectId(creator_id),
                                                projectId=ObjectId(image_group['projectId']),
                                                desc=image_group['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(ImageGroup.objects(name=name).first())

    @staticmethod
    def get_by_id(group_id):
        return convert_mongo_to_json(ImageGroup.objects(id=ObjectId(group_id), isDeleted=False).first())

    @staticmethod
    def get_groups(project_id):
        status = 'ok'
        try:
            rs = ImageGroup.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
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
        return convert_queryset_to_json(ImageGroup.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def update(image_group):
        status = 'ok'
        try:
            data = ImageGroup.objects(id=ObjectId(image_group['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=image_group['name'],
                             desc=image_group['desc'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(image_group_id):
        status = 'ok'
        try:
            data = ImageGroup.objects(id=ObjectId(image_group_id), isDeleted=False)
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
