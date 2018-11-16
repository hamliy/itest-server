# encoding: utf-8
"""
@author: han.li
@file  : s_image.py
@time  : 11/5/18 2:02 PM
@dec   : 图片类
"""

from itest.model.m_image import Image
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json, get_images_path
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id
import uuid, os


class ImageService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(image):
        creator_id = get_user_id()
        return convert_mongo_to_json(Image(name=image['name'],
                                           path=image['path'],
                                           imageType=image['imageType'],
                                           creatorId=ObjectId(creator_id),
                                           projectId=ObjectId(image['projectId']),
                                           groupId=ObjectId(image['groupId']),
                                           tags=image['tags'],
                                           desc=image['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(Image.objects(name=name).first())

    @staticmethod
    def get_by_id(image_id):
        return convert_mongo_to_json(Image.objects(id=ObjectId(image_id), isDeleted=False).first())

    @staticmethod
    def get_images(project_id):
        status = 'ok'
        try:
            rs = Image.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_queryset_to_json(rs), status

    @staticmethod
    def save_image(upload):
        name, ext = os.path.splitext(upload.filename)
        if ext.lower() not in ('.png', '.jpg', '.jpeg'):
            return None, 'ext_error'
        # 定义一个图片存放的位置
        path = get_images_path()

        # 图片path和名称
        save_name = str(uuid.uuid1()) + ext
        image_path = os.path.join(path, save_name)

        # Create temporary directory for storing our files
        if not os.path.exists(path):
            os.makedirs(path)

        # 保存图片
        upload.save(image_path, True)
        return image_path, 'ok'

    @staticmethod
    def find(q, project_id):
        """
        模糊查询
        :return:
        """
        return convert_queryset_to_json(Image.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def update(image):
        status = 'ok'
        try:
            data = Image.objects(id=ObjectId(image['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=image['name'],
                             imageType=image['imageType'],
                             desc=image['desc'],
                             tags=image['tags'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except NotUniqueError:
            rs = None
            status = 'not_unique'
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    @staticmethod
    def update_marks(info):
        status = 'ok'
        try:
            data = Image.objects(id=ObjectId(info['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(marks=info['marks'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(image_id):
        status = 'ok'
        try:
            data = Image.objects(id=ObjectId(image_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + image_id
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
