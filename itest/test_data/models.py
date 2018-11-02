# encoding: utf-8
"""
@author: han.li
@file  : models.py.py
@time  : 10/30/18 4:15 PM
@dec   : 测试数据模型
"""
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
from itest.models import Project


class MarkFieldItem(EmbeddedDocument):
    """打标字段定义项"""
    name = StringField()
    field_type = IntField()  # 0 文本 1 位置
    desc = StringField()


class MarkFieldData(Document):
    """打标字段定义数据"""

    meta = {'collection': 'mark_field'}

    project_id = ReferenceField(Project)
    field_items = ListField(EmbeddedDocumentField(MarkFieldItem))
    desc = StringField()


class MarkData(EmbeddedDocument):
    """打标数据"""

    mark_field_items = ListField()
    mark_result = DictField()
    desc = StringField()

class ImageData(Document):
    """图片数据集"""

    meta = {'collection': 'images'}

    project_id = ReferenceField(Project)
    image_name = StringField()  # 图片名
    image_path = StringField()  # 路径
    image_type = IntField()     # 图片类型 0 未设置 1 票据类型 2 证件类 3 文本类
    tags = ListField()          # 图片标签
    marks = ListField(EmbeddedDocumentField(MarkData))          # 达标数据
    desc = StringField()        # 描述


