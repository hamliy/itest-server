# encoding: utf-8
"""
@author: han.li
@file  : s_user.py
@time  : 11/6/18 3:14 PM
@dec   : 用户服务
"""
from itest.model.m_user import User
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from itest.utils.request import get_user_id
from mongoengine.errors import NotUniqueError
from itest.utils.utils import md5
from bson import ObjectId
from mongoengine.queryset.visitor import Q
from datetime import datetime


class UserService(object):
    def __init__(self):
        pass

    @staticmethod
    def create(user):
        return convert_mongo_to_json(User(email=user['email'],
                                          password=md5(user['password']),
                                          name=user['username']).save())

    @staticmethod
    def get_by_email(email):
        return convert_mongo_to_json(User.objects(email=email).first())

    @staticmethod
    def get_by_id(_id):
        return convert_mongo_to_json(User.objects(id=ObjectId(_id)).first())

    @staticmethod
    def get_by_ids(ids):
        return convert_queryset_to_json(User.objects(id__in=ids))

    @staticmethod
    def find(q):
        """
        模糊查询
        :return:
        """
        return convert_queryset_to_json(User.objects(Q(name__icontains=q) | Q(email__icontains=q)))

    @staticmethod
    def update_password(email, password):
        return User.objects(email=email).update_one(password=md5(password))

    @staticmethod
    def update_password_by_old_password(user_id, old_password, new_password):
        rs = User.objects(id=ObjectId(user_id), password=md5(old_password)).modify(password=md5(new_password),
                                                                                   modifiedTime=datetime.utcnow(),
                                                                                   new=True)
        return convert_mongo_to_json(rs)

    @staticmethod
    def update(user):
        user_id = get_user_id()
        data = User.objects(id=ObjectId(user_id))
        try:
            rs = data.modify(name=user['username'], email=user['email'], modifiedTime=datetime.utcnow(), new=True)
        except NotUniqueError:
            rs = None
        return convert_mongo_to_json(rs)
