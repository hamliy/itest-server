# encoding: utf-8
"""
@author: han.li
@file  : s_celery_tasks.py
@time  : 11/20/18 10:05 AM
@dec   : 异步队列任务服务
"""

from itest.service.interface_use_case.s_interface_use_case import InterfaceUseCaseService
from itest.service.interface_use_case.s_interface_use_case_execution import InterfaceUseCaseExecutionService

class CeleryTasksService(object):
    def __init__(self):
        pass

    @staticmethod
    def execute_use_case_task(use_case_id, execution_id):
        """
        执行用例任务
        1 根据用例id获取用例信息并执行调用
        2 根据结果id 更新执行结果
        :param use_case_id:
        :param execution_id:
        :return:
        """
        response, check_result = InterfaceUseCaseService.execute_use_case(use_case_id)
        return InterfaceUseCaseExecutionService.update_execution(execution_id, response, check_result)
