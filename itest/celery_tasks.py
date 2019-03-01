# encoding: utf-8
"""
@author: han.li
@file  : celery_tasks.py
@time  : 11/19/18 1:45 PM
@dec   : 异步执行任务函数
"""
from itest.celery_client import celery_client
from itest.utils.utils import timestamp_to_datetime, get_time_stamp
from itest.utils.runner import run_by_project, run_by_module, run_by_suite
import shutil, os

from httprunner.api import HttpRunner, logger
from itest.service.test_reports.s_test_reports import add_test_reports


@celery_client.task
def main_hrun(testset_path, report_name):
    """
    用例运行
    :param testset_path:
    :param report_name:
    :return:
    """
    logger.setup_logger('INFO')
    runner = HttpRunner(failfast=False)
    runner.run(testset_path)
    shutil.rmtree(testset_path)
    runner.summary = timestamp_to_datetime(runner.summary)
    add_test_reports(runner, report_name=report_name)


@celery_client.task
def project_hrun(name, base_url, project_id):
    """
    异步运行整个项目用例运行
    :param testset_path:
    :param report_name:
    :return:
    """
    logger.setup_logger('INFO')
    runner = HttpRunner(failfast=False)
    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    # 创建测试用例集
    run_by_project(project_id, base_url, testcase_dir_path)

    runner.run(testcase_dir_path)
    shutil.rmtree(testcase_dir_path)

    runner.summary = timestamp_to_datetime(runner.summary)
    add_test_reports(runner, report_name=name)


@celery_client.task
def module_hrun(name, base_url, modules):
    """
    异步运行整个模块用例
    :param testset_path:
    :param report_name:
    :return:
    """
    logger.setup_logger('INFO')
    runner = HttpRunner(failfast=False)

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    # 创建测试用例集
    try:
        for module in modules:
            run_by_module(module, base_url, testcase_dir_path)
    except Exception:
        return '找不到模块信息'

    runner.run(testcase_dir_path)
    shutil.rmtree(testcase_dir_path)

    runner.summary = timestamp_to_datetime(runner.summary)
    add_test_reports(runner, report_name=name)


@celery_client.task
def suite_hrun(name, base_url, modules):
    """
    异步运行特定用例集合
    :param testset_path:
    :param report_name:
    :return:
    """
    logger.setup_logger('INFO')
    runner = HttpRunner(failfast=False)

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    # 创建测试用例集
    try:
        for module in modules:
            run_by_suite(module, base_url, testcase_dir_path)
    except Exception:
        return '找不到模块信息'

    runner.run(testcase_dir_path)
    shutil.rmtree(testcase_dir_path)

    runner.summary = timestamp_to_datetime(runner.summary)
    add_test_reports(runner, report_name=name)

