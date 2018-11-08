# encoding: utf-8
"""
@author: han.li
@file  : m_image.py
@time  : 11/5/18 10:57 AM
@dec   : 图片类
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_project import Project


class Image(Document):
    """
    接口分组
    """
    meta = {'collection': 'image'}

    projectId = ReferenceField(Project)         # 所属项目id
    name = StringField(required=True)        # 图片名
    path = StringField()  # 路径
    image_type = IntField()     # 图片类型 0 未设置 1 票据类型 2 证件类 3 文本类
    tags = ListField()          # 图片标签
    marks = ListField()          # 标签数据

    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                      # 是否删除
    desc = StringField()                            # 分组描述
