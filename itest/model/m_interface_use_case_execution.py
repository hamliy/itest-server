# encoding: utf-8
"""
@author: han.li
@file  : m_interface_use_case_execution.py
@time  : 11/5/18 11:02 AM
@dec   : 用例执行结果
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from requests import Response
from .m_interface_use_case import InterfaceUseCase
from .m_user import User


class ResponseData(EmbeddedDocument):
    """
    结果数据
    """
    status = IntField()         # 状态码 5001符合异常， 正常错误码
    data = DictField()          # 返回数据
    costTime = FloatField()     # 请求耗时
    errorInfo = StringField()   # 失败详情


class CheckResult(EmbeddedDocument):
    """
    结果数据
    """
    passed = BooleanField()         # 是否通过
    error = StringField()           # 失败信息
    errorDetail = ListField()       # 失败详情


class InterfaceUseCaseExecution(Document):
    """
    用例执行结果
    """
    meta = {'collection': 'interface_use_case_execution'}
    creatorId = ReferenceField(User)  # 执行人
    useCaseId = ReferenceField(InterfaceUseCase)  # 用例Id
    relationId = ObjectIdField(default=None)  # 关联Id  根据执行类型设置 0 无， 1，2 测试计划执行结果 id
    executeType = IntField(default=0)    # 用例执行类型   0 单用例执行调试 1 按组执行 创建临时执行测试计划 2 按测试计划执行
    status = IntField(default=0)    # 用例执行状态 0 执行中 1 执行完成
    useCaseName = StringField(required=True)  # 用例名
    useCaseDesc = StringField()   # 用例

    response = EmbeddedDocumentField(ResponseData)  # 请求信息
    result = EmbeddedDocumentField(CheckResult)    # 信息结果

    startTime = DateTimeField(default=None)  # 开始时间
    endTime = DateTimeField(default=None)  # 结束时间

