# encoding: utf-8
"""
@author: han.li
@file  : config.py
@time  : 2018/8/15 13:50
@dec   : app配置信息
"""
import os


class Config(object):
    """Base configuration"""

    SECRET_KEY = os.environ.get('KYLIN-SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # this directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13 # flask-bcrypt
    DEBUG_TB_ENABLED = False #  Diable Debug

    JWT_SECRET_KEY = 'super-secret'

    # 请求的json返回字符串显示中文
    JSON_AS_ASCII = False
    # 开启访问拦截
    BEFORE_REQUEST = False
    # 开启过期时间验证
    VERIFY_EXP = True

class ProdConfig(Config):
    """Prodction configuration"""

    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False
    MONGO_URI = 'mongodb://172.20.166.50:27017/butterfly'
    MONGO_USERNAME = 'kingdee'
    MONGO_PASSWORD = 'kingdee'


class DevConfig(Config):
    """Development configuration"""

    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    #MONGO_HOST = 'localhost'
    #MONGO_PORT = 27017
    MONGO_URI = 'mongodb://172.20.166.50:27017/itest2'
    # MONGO_USERNAME = 'kingdee'
    # MONGO_PASSWORD = 'kingdee'
    # MONGO_DBNAME = 'butterfly'
    # MONGO_USERNAME = 'kingdee'
    # MONGO_PASSWORD = 'kingdee'


class TestConfig(Config):
    """Test configuration"""

    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    MONGO_URI = 'mongodb://127.0.0.1:27017/butterfly'
    MONGO_USERNAME = 'kingdee'
    MONGO_PASSWORD = 'kingdee'


