# encoding: utf-8
"""
@author: han.li
@file  : models.py
@time  : 8/28/18 10:16 AM
@dec   : 
"""
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, DictField, FloatField, IntField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
import json

"""
    发票相关mongo数据库
    1 发票数据集合
    2 接口调用集合
    3 发票任务集合
"""


class Five(EmbeddedDocument):
    """发票五要素"""
    fpdm = StringField()        # 发票代码
    fphm = StringField()        # 发票号码
    kprq = StringField()        # 发票日期
    fpje = StringField()        # 发票金额
    jym = StringField()         # 发票校验码

class Invoice(Document):
    """  1 发票数据集合"""

    meta = {'collection': 'invoices'}

    id = ObjectIdField(name='_id')
    image_name = StringField()  # 发票图片名
    image_path = StringField()  # 发票路径
    image_from = IntField()        # 发票来源（0-扫描/1-拍照）
    checked = BooleanField()        # 是否已校验
    detail = EmbeddedDocumentField(Five)  # 发票五要素

    def to_dict(self):
        data = self.to_json()
        data = json.loads(data)
        data['id'] = data["_auto_id_0"]['$oid']
        data.pop('_auto_id_0')
        return data





