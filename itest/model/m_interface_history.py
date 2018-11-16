# encoding: utf-8
"""
@author: han.li
@file  : m_interface_history.py
@time  : 11/5/18 3:57 PM
@dec   : 接口修改历史记录
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField, SortedListField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_interface import Interface
from .m_user import User


class History(EmbeddedDocument):
    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    data = DictField()
    operatorId = ReferenceField(User)
    operatorName = StringField()


class InterfaceHistory(Document):
    """
       接口信息
       """
    meta = {'collection': 'interface_history'}

    interfaceId = ReferenceField(Interface, required=True, unique=True)   # 关联接口
    records = SortedListField(EmbeddedDocumentField(History), default=[], ordering="createTime", reverse=True)
    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)  # 更新时间


