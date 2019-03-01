# encoding: utf-8
"""
@author: han.li
@file  : m_project.py
@time  : 11/5/18 2:35 PM
@dec   : 项目类
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField
)

from .m_user import User


class Project(Document):
    """
    项目信息
    """
    meta = {'collection': 'db_project'}

    name = StringField(required=True, unique=True)      # 项目名
    version = StringField(default="V1.0")                             # 项目版本号 V1.0 后续创建版本管理
    creatorId = ReferenceField(User)                      # 创建人
    devUser = StringField(default='')
    testUser = StringField(default='')

    createTime = DateTimeField(default=datetime.utcnow)                        # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                      # 更新时间
    isDeleted = BooleanField(default=False)                          # 是否删除
    desc = StringField(default="")                                # 描述
