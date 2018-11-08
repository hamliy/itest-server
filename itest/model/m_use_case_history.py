# encoding: utf-8
"""
@author: han.li
@file  : m_use_case_history.py
@time  : 11/5/18 8:52 PM
@dec   : 用例执行历史
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_use_case import UseCase
from .m_user import User


class History(EmbeddedDocument):
    createTime = DateTimeField(default=datetime.utcnow())  # 创建时间
    data = DictField()
    operator = ReferenceField(User)
    operatorName = StringField()


class UseCaseHistory(Document):
    """
   用例修改历史
   """
    meta = {'collection': 'use_case_history'}

    interfaceId = ReferenceField(UseCase)   # 关联接口
    records = ListField(EmbeddedDocumentField(History))
    createTime = DateTimeField(default=datetime.utcnow())  # 创建时间
    updateTime = DateTimeField(default=datetime.utcnow())  # 更新时间
