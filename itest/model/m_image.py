# encoding: utf-8
"""
@author: han.li
@file  : m_image.py
@time  : 11/5/18 10:57 AM
@dec   : 图片类
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_project import Project
from .m_image_group import ImageGroup
from .m_user import User


class Image(Document):
    """
    图片数据
    """
    meta = {'collection': 'image'}

    projectId = ReferenceField(Project)         # 所属项目id
    name = StringField(required=True)        # 图片名  图片名可以重复
    path = StringField(required=True, unique=True)  # 路径 唯一
    groupId = ReferenceField(ImageGroup)    # 图片分组id
    imageType = IntField(default=0)     # 图片类型 0 未设置 1 票据类型 2 证件类 3 文本类
    tags = ListField(default=[])          # 图片标签
    marks = ListField(default=[])          # 标签数据 文本 text:[{key:value}] 位置 location:[{location:{x,y,w,h},text:text}]

    creatorId = ReferenceField(User)  # 创建人
    createTime = DateTimeField(default=datetime.utcnow)                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField(default="")                            # 分组描述
