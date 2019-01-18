# encoding: utf-8
"""
@author: han.li
@file  : m_test_suite.py
@time  : 1/15/19 2:18 PM
@dec   : 
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField
)

from .m_user import User
from .m_project import Project


class TestSuite(Document):
    """
    用例集合
    """
    meta = {'collection': 'db_test_suite'}

    name = StringField(required=True, unique=True)  # 集合名
    belongProjectId = ReferenceField(Project)  # 所属项目
    creatorId = ReferenceField(User)  # 创建人
    include = StringField()     # 前置config/test

    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)  # 更新时间
    isDeleted = BooleanField(default=False)  # 是否删除
    desc = StringField(default="")      # 描述
