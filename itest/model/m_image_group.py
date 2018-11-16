# encoding: utf-8
"""
@author: han.li
@file  : m_image_group.py
@time  : 11/14/18 2:37 PM
@dec   : 图片分组
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_project import Project
from .m_user import User


class ImageGroup(Document):
    """
    图片分组
    """
    meta = {'collection': 'image_group'}

    projectId = ReferenceField(Project)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    name = StringField(required=True)               # 组名
    member = ListField(ObjectIdField(), default=[])
    createTime = DateTimeField(default=datetime.utcnow)                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    level = IntField(required=True, default=1)      # 分组层级 默认 1级
    desc = StringField(default="")                            # 分组描述

