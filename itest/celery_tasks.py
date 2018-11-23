# encoding: utf-8
"""
@author: han.li
@file  : celery_tasks.py
@time  : 11/19/18 1:45 PM
@dec   : 异步执行任务函数
"""
from itest.celery_client import celery_client
from itest.service.celery_tasks.s_celery_tasks import CeleryTasksService


@celery_client.task
def add(x, y):
    return x+y


@celery_client.task
def execute_use_case_task(use_case_id, execution_id):
    return CeleryTasksService.execute_use_case_task(use_case_id, execution_id)


