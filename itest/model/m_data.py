# encoding: utf-8
"""
@author: han.li
@file  : m_data.py
@time  : 11/5/18 10:58 AM
@dec   : 数据类 图片+标签
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_user import User
from .m_project import Project


class Data(Document):
    """
    数据集
    """
    meta = {'collection': 'data'}

    projectId = ReferenceField(Project)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    name = StringField(required=True)                   # 数据集名
    dataList = ListField()                             # 数据集

    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField()                                    # 描述
