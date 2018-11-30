# encoding: utf-8
"""
@author: han.li
@file  : s_token.py
@time  : 11/27/18 2:56 PM
@dec   : token 服务
"""
from itest.model.m_token import Token
from datetime import datetime
from datetime import timedelta
from flask_jwt_extended import decode_token


class TokenService(object):
    def __init__(self):
        pass

    @staticmethod
    def _epoch_utc_to_datetime(epoch_utc):
        return datetime.fromtimestamp(epoch_utc) + timedelta(hours=-8)  # 中国默认时区

    @staticmethod
    def get_token_exp(encoded_token):
        decoded_token = decode_token(encoded_token)
        return TokenService._epoch_utc_to_datetime(decoded_token['exp'])

    @staticmethod
    def add_token_to_database(encoded_token, identity_claim):
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        user_identity = decoded_token[identity_claim]
        expires = TokenService._epoch_utc_to_datetime(decoded_token['exp'])
        revoked = False
        Token(
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked,
        ).save()

    def is_token_revoked(decoded_token):
        """
        Checks if the given token is revoked or not. Because we are adding all the
        tokens that we create into this database, if the token is not present
        in the database we are going to consider it revoked, as we don't know where
        it was created.
        """
        jti = decoded_token['jti']
        token = Token.objects(jti=jti).first()
        if token:
            return token.revoked
        return True

    @staticmethod
    def get_user_tokens(user_identity):
        return Token.objects(user_identity=user_identity)

    @staticmethod
    def revoke_token(jti, user):
        """
        Revokes the given token. Raises a TokenNotFound error if the token does
        not exist in the database
        """
        Token.objects(jti=jti, user_identity=user).modify(revoked=True)

    @staticmethod
    def unrevoke_token(token_id, user):
        """
        Unrevokes the given token. Raises a TokenNotFound error if the token does
        not exist in the database
        """
        token = Token.objects(id=token_id, user_identity=user).first()
        token.revoked = False

    @staticmethod
    def prune_database():
        """
        Delete tokens that have expired from the database.
        How (and if) you call this is entirely up you. You could expose it to an
        endpoint that only administrators could call, you could run it as a cron,
        set it up with flask cli, etc.
        """
        now = datetime.now()
        expired = Token.objects(expires__lt=now).all()
        for token in expired:
            Token.delete(token)
