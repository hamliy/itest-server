# encoding: utf-8
"""
@author: han.li
@file  : m_test_case.py
@time  : 1/15/19 2:17 PM
@dec   : 用例信息
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField, IntField, DictField
)

from .m_project import Project
from .m_user import User
from .m_module import Module


LEVEL = (0, 1, 2, 3, 4)


class TestCase(Document):
    """
    用例信息
    """
    meta = {'collection': 'db_test_case'}

    name = StringField(required=True, max_length=50)  # 用例/配置名称
    configType = IntField(default=1)    # 'test/config'
    belongProjectId = ReferenceField(Project)  # 所属项目
    creatorId = ReferenceField(User)                  # 创建人id
    belongModuleId = ReferenceField(Module, reverse_delete_rule='CASCADE')  # 所属模块, 如果模块删除 者相关用例也删除
    include = StringField()                 # 前置config/test
    level = IntField(required=True, default=0, choices=LEVEL)  # 用例级别 0 未设置  1 2 3 4

    request = DictField(required=True)  # 用例请求

    createTime = DateTimeField(default=datetime.utcnow)                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField()                                    # 描述

