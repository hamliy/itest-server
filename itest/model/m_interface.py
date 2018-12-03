# encoding: utf-8
"""
@author: han.li
@file  : m_interface.py
@time  : 11/5/18 10:57 AM
@dec   : 接口类
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_user import User
from .m_project import Project
from .m_interface_group import InterfaceGroup


class BodyParam(EmbeddedDocument):
    """
    内容参数
    """

    body = ListField()      # 提交 json 或form数据  请求类型为GET 则无该参数 data
    path = ListField()      # 提交 restful风格url参数 https://www/:param1/:param2 url
    query = ListField()     # url参数 https://www？param1=hi params
    type = IntField(default=0)  # 类型 0 body 1 path 2 query


class BodyExample(EmbeddedDocument):
    """
    内容示例 json 对象
    """

    body = DictField(default=None)
    path = DictField(default=None)
    query = DictField(default=None)


class HeaderParam(EmbeddedDocument):
    """
    请求头内容
    """
    name = StringField()      # 名称
    value = StringField()   # 值
    desc = StringField()    # 描述


class ResponseParams(EmbeddedDocument):
    """
    返回结果内容
    """
    example = DictField()       # 示例
    params = ListField()        # 返回参数
    status = IntField()          # 状态码
    statusText = StringField()   # 状态名


class Option(EmbeddedDocument):
    """
    接口参数
    """
    headers = ListField(EmbeddedDocumentField(HeaderParam))
    params = EmbeddedDocumentField(BodyParam)
    example = EmbeddedDocumentField(BodyExample)
    response = ListField(EmbeddedDocumentField( ))
    responseIndex = IntField(default=0)      # 指定返回结果 或随机
    delay = IntField(default=0)             # 模拟网络延迟


class Interface(Document):
    """
    接口信息
    """
    meta = {'collection': 'interfaces'}

    projectId = ReferenceField(Project)  # 所属项目id
    groupId = ReferenceField(InterfaceGroup)   # 所属组
    creatorId = ReferenceField(User)  # 创建人id
    name = StringField(required=True)  # 接口名
    method = StringField(required=True, default="GET")  # 方法
    path = StringField(required=True)   # 接口路径
    option = EmbeddedDocumentField(Option)

    createTime = DateTimeField(default=datetime.utcnow)  # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)  # 更新时间
    isDeleted = BooleanField(default=False)  # 是否删除
    desc = StringField(default="")  # 分组描述



