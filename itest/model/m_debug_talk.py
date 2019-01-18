# encoding: utf-8
"""
@author: han.li
@file  : m_debug_talk.py
@time  : 1/15/19 2:17 PM
@dec   : 驱动py文件
"""

from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField
)

from .m_user import User
from .m_project import Project


class DebugTalk(Document):
    """
    项驱动py文件
    """
    meta = {'collection': 'db_debug_talk'}

    name = StringField(required=True, unique=True)  # 项目名
    belongProjectId = ReferenceField(Project)  # 所属项目
    creatorId = ReferenceField(User)  # 创建人
    debugTalk = StringField(default='#debugtalk.py')  # 文件名位置

    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)  # 更新时间
    isDeleted = BooleanField(default=False)  # 是否删除
    desc = StringField(default="")      # 描述
