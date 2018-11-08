# encoding: utf-8
"""
@author: han.li
@file  : m_mark.py
@time  : 11/5/18 10:58 AM
@dec   : 数据标签类
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)

from .m_project import Project
from .m_image import Image


class Mark(Document):
    """
    图片标签数据
    """
    meta = {'collection': 'mark'}

    projectId = ReferenceField(Project)         # 所属项目id
    imageId = ReferenceField(Image)          # 所属图片
    name = StringField(required=True)        # 标签名
    mark_type = IntField(default=0)         # 标签类型 0 文本   {key:value}  1 位置 {location:{x, y, w,h}, text:text}
    data = ListField()                      # 标签数据

    createTime = DateTimeField(default=datetime.utcnow())                    # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                  # 更新时间
    isDeleted = BooleanField(default=False)                     # 是否删除
    desc = StringField()                                        # 描述
