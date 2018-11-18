# encoding: utf-8
"""
@author: han.li
@file  : m_test_plan_execution.py
@time  : 11/5/18 8:49 PM
@dec   : 任务执行结果
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_test_plan import TestPlan


class TestPlanDetail(EmbeddedDocument):
    """
    任务执行数据
    """
    total = IntField()                               # 总用例数
    queue = ListField()                              # 待执行用例队列
    passed = IntField()    # 执行成功用例数
    failed = IntField()    # 执行失败用例数
    costTime = FloatField()                         # 耗时


class TestPlanExecution(Document):
    """
    任务执行结果
    """
    meta = {'collection': 'task_execution'}

    testPlanId = ReferenceField(TestPlan)
    testPlanName = StringField(required=True)   # 测试计划名
    relationId = ObjectIdField(default=None)  # 关联Id  根据执行类型设置 0 测试计划id， 1 接口分组 id
    executeType = IntField(default=0)                # 用例执行类型 0 按测试计划执行  1 按组执行 创建临时执行测试计划
    desc = StringField(default="")              # 测试计划执行描述
    detail = EmbeddedDocumentField(TestPlanDetail)  # 信息结果

    startTime = DateTimeField(default=datetime.utcnow)  # 开始时间
    endTime = DateTimeField(default=datetime.utcnow)  # 结束时间
