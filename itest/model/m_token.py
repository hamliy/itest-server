# encoding: utf-8
"""
@author: han.li
@file  : m_token.py
@time  : 11/27/18 2:47 PM
@dec   : 失效token
"""
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, StringField, BooleanField
)


class Token(Document):
    """
    任务执行结果
    """
    meta = {'collection': 'token'}

    jti = StringField()
    token_type = StringField()
    user_identity = StringField()
    revoked = BooleanField()
    expires = DateTimeField()

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }
