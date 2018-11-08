# encoding: utf-8
"""
@author: han.li
@file  : m_use_case.py
@time  : 11/5/18 10:56 AM
@dec   : 用例类 接口+数据+环境
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_user import User
from .m_project import Project
from .m_interface import Interface
from .m_environment import Environment


class UseCaseOption(EmbeddedDocument):
    """
    用例参数
    """
    path = StringField()                # 接口路径
    method = StringField()              # 方法
    headers = ListField()               # 请求头
    params = DictField()                # 请求参数

    expect = DictField()                # 用例预期结果
    checkRule = DictField()             # 预期结果校验规则
    association = DictField()           # 参数关联  {useCaseId:id, data: data} setup tearDown
    delay = IntField(default=0)         # 模拟网络延迟


class UseCase(Document):
    """
    用例
    """
    meta = {'collection': 'use_case'}

    projectId = ReferenceField(Project)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    interfaceId = ReferenceField(Interface)
    environmentId = ReferenceField(Environment)
    useCaseNo = StringField()                           # 用例编号
    name = StringField(required=True)                   # 用例名
    detail = StringField()                              # 用例详情

    options = EmbeddedDocumentField(UseCaseOption)      # 用例参数

    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField()                                    # 描述
