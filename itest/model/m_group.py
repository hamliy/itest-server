# encoding: utf-8
"""
@author: han.li
@file  : m_group.py
@time  : 11/5/18 2:55 PM
@dec   : 
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_user import User
from .m_project import Project
from .m_interface import Interface


class Group(Document):
    """
    接口分组
    """
    meta = {'collection': 'group'}

    projectId = ReferenceField(Project)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    name = StringField(required=True)               # 组名
    member = ListField(ReferenceField(Interface))             # 接口成员
    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    level = IntField(required=True, default=1)      # 分组层级 默认 1级
    desc = StringField()                            # 分组描述