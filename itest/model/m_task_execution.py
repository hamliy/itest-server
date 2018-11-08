# encoding: utf-8
"""
@author: han.li
@file  : m_task_execution.py
@time  : 11/5/18 8:49 PM
@dec   : 任务执行结果
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_task import Task


class TaskDetail(EmbeddedDocument):
    """
    任务执行数据
    """
    total = IntField()                               # 总用例数
    queue = ListField()                              # 待执行用例队列
    passed = IntField()    # 执行成功用例数
    failed = IntField()    # 执行失败用例数
    costTime = FloatField()                         # 耗时


class TaskExecution(Document):
    """
    任务执行结果
    """
    meta = {'collection': 'task_execution'}

    taskId = ReferenceField(Task)
    taskName = StringField(required=True)  # 用例名
    detail = EmbeddedDocumentField(TaskDetail)  # 信息结果

    startTime = DateTimeField(default=datetime.utcnow())  # 开始时间
    endTime = DateTimeField(default=datetime.utcnow())  # 结束时间
