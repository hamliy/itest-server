# encoding: utf-8
"""
@author: han.li
@file  : m_module.py
@time  : 1/15/19 2:17 PM
@dec   : 模块信息
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField
)

from .m_project import Project
from .m_user import User


class Module(Document):
    """
    项目模块信息
    """
    meta = {'collection': 'db_module'}

    name = StringField(required=True, unique=True)      # 模块名
    belongProjectId = ReferenceField(Project)           # 所属项目
    creatorId = ReferenceField(User)                    # 创建人
    testUser = StringField(default='')                  # 测试人员名

    createTime = DateTimeField(default=datetime.utcnow)                        # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                      # 更新时间
    isDeleted = BooleanField(default=False)                          # 是否删除
    desc = StringField(default="")                                # 描述
