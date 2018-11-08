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
    DateTimeField, StringField, BooleanField
)


class User(Document):
    """
    用户信息
    """
    meta = {'collection': 'user'}

    name = StringField(required=True)                   # 用户名
    email = StringField(required=True, unique=True)     # 邮箱
    password = StringField(required=True)               # 密码
    createTime = DateTimeField(default=datetime.utcnow())                        # 创建时间
    modifiedTime = DateTimeField(default=datetime.utcnow())                      # 更新时间
    isDeleted = BooleanField(default=False)                          # 是否删除
