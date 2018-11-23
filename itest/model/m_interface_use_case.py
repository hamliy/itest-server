# encoding: utf-8
"""
@author: han.li
@file  : m_interface_use_case.py
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
from .m_interface_use_case_group import InterfaceUseCaseGroup


class InterfaceUseCaseOption(EmbeddedDocument):
    """
    用例参数
    """
    url = StringField()                 # 请求url
    path = StringField()                # 接口路径
    method = StringField()              # 方法
    headers = DictField()               # 请求头
    params = DictField()                # 请求参数
    data = DictField(default=None)                  # 请求数据
    files = DictField(default=None)                 # 请求文件 {name: image_id} 换成图片i
    request_type = IntField(default=0)  # post请求类型 => 0: params or forms, 1: json , 2: files
    # file_type = IntField(default=0)     # 文件类型  0: 文件 1： 文件转 Base64 2： 直接Base64

    expect = DictField()                # 用例预期结果
    checkRule = DictField()             # 预期结果校验规则
    association = DictField()           # 参数关联  {useCaseId:id, data: data} setup tearDown
    delay = IntField(default=0)         # 模拟网络延迟


class InterfaceUseCase(Document):
    """
    用例
    """
    meta = {'collection': 'interface_use_case'}

    projectId = ReferenceField(Project, required=True)             # 所属项目id
    creatorId = ReferenceField(User)                  # 创建人id
    interfaceId = ReferenceField(Interface)
    environmentId = ReferenceField(Environment)
    groupId = ReferenceField(InterfaceUseCaseGroup)     # 用例分组
    useCaseNo = StringField(required=True, unique=True)                           # 用例编号
    level = IntField(required=True, default=0)  # 用例级别 0 未设置  1 2 3 4
    name = StringField(required=True)                   # 用例名
    detail = StringField(required=True, defalt="")                              # 用例详情

    option = EmbeddedDocumentField(InterfaceUseCaseOption)      # 用例参数

    createTime = DateTimeField(default=datetime.utcnow)                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField()                                    # 描述
