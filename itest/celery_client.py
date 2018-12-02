# encoding: utf-8
"""
@author: han.li
@file  : celery_client.py
@time  : 11/19/18 11:19 AM
@dec   : 异步调用 客户端
"""

from celery import Celery

from mongoengine import connect


def init_mongo():
    try:
        connect('itest', host='mongodb://localhost:27017/itest-dev', connect=False)
    except Exception:
        raise Exception('连接数据库失败')


celery_client = Celery('itest', include=['itest.celery_tasks'])
celery_client.config_from_object('itest.celery_config')
init_mongo()


# 启动 celery -A itest.celery_client worker -l info
if __name__ == '__main__':
    celery_client.start()
