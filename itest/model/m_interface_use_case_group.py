#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/11/18 下午4:49
# @Author  : lihan
# @File    : m_interface_use_case_group.py
# @Dec     : 接口用例分组

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_user import User
from .m_project import Project

class InterfaceUseCaseBase(EmbeddedDocument):

    id = ObjectIdField()
    name = StringField()

class InterfaceUseCaseGroup(Document):
    """
    接口用例分组
    """
    meta = {'collection': 'interface_use_case_group'}

    projectId = ReferenceField(Project)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    name = StringField(required=True)               # 组名
    member = ListField(EmbeddedDocumentField(InterfaceUseCaseBase), default=[])             # 用例成员
    groupType = IntField(default=0)                 # 分组类型默认  0 ，接口用例组，成员 无关联执行
                                                    # 1 业务用例组，用例上下文，按顺序执行
    createTime = DateTimeField(default=datetime.utcnow)                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    level = IntField(required=True, default=1)      # 分组层级 默认 1级
    desc = StringField(default="")                            # 分组描述