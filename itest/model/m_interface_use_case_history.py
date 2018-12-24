# encoding: utf-8
"""
@author: han.li
@file  : m_interface_use_case_history.py
@time  : 11/5/18 8:52 PM
@dec   : 用例执行历史
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_interface_use_case import InterfaceUseCase
from .m_user import User


class History(EmbeddedDocument):
    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    data = DictField()
    operatorId = ReferenceField(User)
    operatorName = StringField()


class InterfaceUseCaseHistory(Document):
    """
   用例修改历史
   """
    meta = {'collection': 'interface_use_case_history'}

    useCaseId = ReferenceField(InterfaceUseCase, unique=True)        # 关联用例
    records = ListField(EmbeddedDocumentField(History))
    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)  # 更新时间
