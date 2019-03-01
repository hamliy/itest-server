# encoding: utf-8
"""
@author: han.li
@file  : celery_config.py
@time  : 11/19/18 1:38 PM
@dec   : 异步任务配置
"""
# 把结果存在Redis
CELERY_RESULT_BACKEND = 'mongodb://172.20.166.50:27017/celery'
# 任务序列化和反序列化使用JSON方案
CELERY_TASK_SERIALIZER = 'json'
# 读取任务结果使用JSON
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间，不建议直接写86400, 应该让这样的magic数字表达更明显
CELERY_TASK_RESULT_EXPIRES = 60*60*24
# 指定接受的内容类型，是数组，可以写多个
CELERY_ACCEPT_CONTENT = ['json']


