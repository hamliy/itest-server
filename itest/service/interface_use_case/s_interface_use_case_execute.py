# encoding: utf-8
"""
@author: han.li
@file  : s_interface_use_case_execute.py
@time  : 11/20/18 1:44 PM
@dec   : 用例执行服务
"""
from itest.service.interface_use_case.s_interface_use_case_execution import InterfaceUseCaseExecutionService
from itest.service.interface_use_case.s_interface_use_case_group import InterfaceUseCaseGroupService
from bson.errors import InvalidId
from itest.celery_tasks import execute_use_case_task
from celery import group


class InterfaceUseCaseExecuteService(object):
    def __init__(self):
        pass

    @staticmethod
    def execute_by_id(use_case_id):
        """
        执行用例： 1 创建用例执行结果 2 调用异步任务 执行用例 3 返回任务开始状态
        :param use_case_id:
        :return:
        """
        execution = InterfaceUseCaseExecutionService.create_execution_by_id(use_case_id)
        # 按组执行单个用例任务
        print(use_case_id, execution['id'])
        execute_use_case_task.delay(use_case_id, execution['id'])
        return execution

    @staticmethod
    def execute_by_group(group_id):
        """
        执行用例：
        1 创建用例执行结果
        2 调用异步任务 执行用例
        3 返回任务开始状态
        :param group_id:
        :return:
        """
        status = 'ok'
        try:
            executions = InterfaceUseCaseExecutionService.create_execution_by_group(group_id)
        except InvalidId:
            return None, 'not_object_id'

        g = group(execute_use_case_task.s(str(execution['useCaseId']), str(execution['id']))
                  for execution in executions)()
        g.save()
        return executions, status

    @staticmethod
    def execute_by_test_plan(test_plan_id):
        """
        执行用例：
        1 创建用例执行结果
        2 调用异步任务 执行用例
        3 返回任务开始状态
        :param test_plan_id:
        :return:
        """
        status = 'ok'
        try:
            executions = InterfaceUseCaseExecutionService.create_execution_by_group(test_plan_id)
        except InvalidId:
            return None, 'not_object_id'

        g = group(execute_use_case_task.s(str(execution['useCaseId']), str(execution['id']))
                  for execution in executions)()
        g.save()
        return executions, status

