# encoding: utf-8
"""
@author: han.li
@file  : m_mark_field.py
@time  : 11/5/18 10:58 AM
@dec   : 数据标签字段类
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_project import Project



class MarkFieldItem(EmbeddedDocument):
    """打标字段定义项"""
    name = StringField()        # 标签字段名
    itemType = IntField(default=0)    # 数据类型 0 字符串 1 数字 2 list
    desc = StringField()        # 描述


class MarkField(Document):
    """打标字段定义数据"""

    meta = {'collection': 'mark_field'}

    projectId = ReferenceField(Project)
    name = StringField(required=True)                                   # 标签定义名
    fieldType = IntField(required=True, default=0)                      # 标签类型 0 文本 1 位置 2 文本+位置

    fieldItems = ListField(EmbeddedDocumentField(MarkFieldItem), default=[])   # 标签字段定义

    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                     # 是否删除
    desc = StringField(default="")                                        # 描述
