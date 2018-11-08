# encoding: utf-8
"""
@author: han.li
@file  : m_use_case_execution.py
@time  : 11/5/18 11:02 AM
@dec   : 用例执行结果
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from .m_use_case import UseCase
from .m_task_execution import TaskExecution


class ResponseData(EmbeddedDocument):
    """
    结果数据
    """
    status = IntField()         # 状态码
    data = DictField()          # 返回数据
    costTime = FloatField()     # 请求耗时


class CheckResult(EmbeddedDocument):
    """
    结果数据
    """
    passed = BooleanField()         # 是否通过
    error = StringField()           # 失败信息
    errorDetail = DictField()       # 失败详情


class UseCaseExecution(Document):
    """
    用例执行结果
    """
    meta = {'collection': 'use_case_execution'}

    useCaseId = ReferenceField(UseCase)  # 用例Id
    taskExecutionId = ReferenceField(TaskExecution)  # 任务执行结果
    useCaseNo = StringField()  # 用例编号
    useCaseName = StringField(required=True)  # 用例名
    useCaseDetail = StringField()   # 用例

    response = EmbeddedDocumentField(ResponseData)  # 请求信息
    result = EmbeddedDocumentField(CheckResult)    # 信息结果

    startTime = DateTimeField(default=datetime.utcnow())  # 开始时间
    endTime = DateTimeField(default=datetime.utcnow())  # 结束时间

