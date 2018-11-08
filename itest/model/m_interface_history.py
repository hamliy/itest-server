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
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_interface import Interface
from .m_user import User


class History(EmbeddedDocument):
    createTime = DateTimeField(default=datetime.utcnow())  # 创建时间
    data = DictField()
    operator = ReferenceField(User)
    operatorName = StringField()


class InterfaceHistory(Document):
    """
       接口信息
       """
    meta = {'collection': 'interface_history'}

    interfaceId = ReferenceField(Interface)   # 关联接口
    records = ListField(EmbeddedDocumentField(History))
    createTime = DateTimeField(default=datetime.utcnow())  # 创建时间
    updateTime = DateTimeField(default=datetime.utcnow())  # 更新时间


