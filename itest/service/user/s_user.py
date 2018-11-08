# encoding: utf-8
"""
@author: han.li
@file  : s_user.py
@time  : 11/6/18 3:14 PM
@dec   : 用户服务
"""
from itest.model.m_user import User

from itest.config import DevConfig
from itest.utils.utils import md5
from bson import ObjectId

class UserService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(user):
        return User(email=user.email, password=md5(user.password), name=user.name)

    @staticmethod
    def get_by_email(email):
        return User.objects(email=email).first()

    def get_by_id(id):
        return User.objects(_id=ObjectId(id)).first()

    def get_by_ids(ids):
        return User.objects(_id__in=ids)

    def update(self):
        pass

    def query(self):
        pass
