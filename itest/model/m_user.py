# encoding: utf-8
"""
@author: han.li
@file  : m_user.py
@time  : 11/5/18 2:47 PM
@dec   : 用户信息
"""
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField, IntField
)
from itest.utils.decorators import model_handler
from mongoengine import signals


# @model_handler(signals.pre_save)
# def update_modified(sender, document, **kwargs):
#     print(type(kwargs), kwargs)
#     print(type(sender), sender)
#     print(type(document),document)
#     document.modifiedTime = datetime.utcnow()
#
#
# @update_modified.apply
class User(Document):
    """
    用户信息
    """
    meta = {'collection': 'user'}

    name = StringField(required=True)                   # 用户名
    email = StringField(required=True, unique=True)     # 邮箱
    password = StringField(required=True)               # 密码

    createTime = DateTimeField(default=datetime.utcnow)                        # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow)                      # 更新时间
    isDeleted = BooleanField(default=False)                          # 是否删除
