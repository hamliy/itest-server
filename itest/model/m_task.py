# encoding: utf-8
"""
@author: han.li
@file  : m_task.py
@time  : 11/5/18 11:01 AM
@dec   : 任务类 N+用例
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField, ListField
)
from .m_project import Project
from .m_use_case import UseCase


class Task(Document):
    """
    任务
    """
    meta = {'collection': 'task'}

    projectId = ReferenceField(Project)         # 所属项目id
    useCaseList = ListField(ReferenceField(UseCase))    # 用例集合
    name = StringField(required=True)                   # 任务名

    createTime = DateTimeField(default=datetime.utcnow())  # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())  # 更新时间
    isDeleted = BooleanField(default=False)  # 是否删除
    desc = StringField()  # 描述
