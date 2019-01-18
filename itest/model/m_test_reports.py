# encoding: utf-8
"""
@author: han.li
@file  : m_test_reports.py
@time  : 1/15/19 2:19 PM
@dec   : 测试报告
"""
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, ReferenceField, DictField
)

from .m_user import User
from .m_project import Project


class TestReports(Document):
    """
    执行结果
    """
    meta = {'collection': 'db_test_reports'}

    name = StringField(required=True, unique=True)  # 集合名
    belongProjectId = ReferenceField(Project)  # 所属项目
    creatorId = ReferenceField(User)  # 创建人
    startTime = DateTimeField()     # 运行时间
    status = BooleanField()     # 任务状态
    stat = DictField()       # 结果 状态 stat

    reports = DictField()    # 执行结果

