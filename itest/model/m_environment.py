# encoding: utf-8
"""
@author: han.li
@file  : m_environment.py
@time  : 11/5/18 10:57 AM
@dec   : 环境类
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_user import User
from .m_project import Project


class Environment(Document):
    """
    环境数据
    """
    meta = {'collection': 'environment'}

    projectId = ReferenceField(Project)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    name = StringField(required=True)                   # 环境名
    path = StringField(required=True)               # 环境路径
    status = IntField()                             # 环境状态 0 ping通 1 ping不通 2 其他
    checkTime = DateTimeField(default=datetime.utcnow())    # 状态检查时间
    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField()                            # 描述
