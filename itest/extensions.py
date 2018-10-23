# encoding: utf-8
"""
@author: han.li
@file  : extensions.py
@time  : 2018/8/15 20:17
@dec   : 扩展组件集
"""
from mongoengine import connect
from flask_cors import CORS
from flask_jwt_extended import JWTManager

cors = CORS()
jwt = JWTManager()

def init_mongo(app, config_prefix='MONGO'):
    def key(suffix):
            return '%s_%s' % (config_prefix, suffix)

    if app is not None:
        if key('URI') in app.config:
            try:
                connect('itest', host=app.config[key('URI')])
            except Exception:
                raise Exception('连接数据库失败')
        else:
            raise Exception('数据库配置未配置正确')
    else:
        raise Exception('初始数据库失败，app 为空')

