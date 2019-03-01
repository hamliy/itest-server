# encoding: utf-8
"""
@author: han.li
@file  : runner.py
@time  : 1/15/19 10:52 AM
@dec   : 运行用例
"""

import os

from bson import ObjectId
from itest.model.m_project import Project
from itest.model.m_module import Module
from itest.model.m_debug_talk import DebugTalk
from itest.model.m_test_case import TestCase
from itest.model.m_test_suite import TestSuite

from itest.utils.utils import dump_python_file, dump_yaml_file


def run_by_single(index, base_url, path):
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    config = {
        'config': {
            'name': '',
            'request': {
                'base_url': base_url
            }
        }
    }

    test_case_list = [config]

    data = TestCase.objects(id=ObjectId(index), isDeleted=False)

    obj = data.first()

    if not obj:
        return test_case_list

    include = eval(obj['include'])
    request = eval(obj['request'])
    name = obj['name']
    project = obj['belongProjectId']
    module = obj['belongModuleId']
    # module = obj.belong_module.module_name

    config['config']['name'] = name

    test_case_dir_path = os.path.join(path, project)

    if not os.path.exists(test_case_dir_path):
        os.makedirs(test_case_dir_path)

        debugtalk_datas = DebugTalk.objects(belongProjectId=project)

        if not debugtalk_datas.first():
            return test_case_list

        debug_talk = debugtalk_datas.first()['debugTalk']

        dump_python_file(os.path.join(test_case_list, 'debugtalk.py'), debug_talk)

    testcase_dir_path = os.path.join(test_case_dir_path, module)

    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)

    for test_info in include:
        if isinstance(test_info, dict):
            config_id = test_info.pop('config')[0]
            config_request = eval(TestCase.objects(id=ObjectId(config_id)).first()['request'])
            config_request.get('config').get('request').setdefault('base_url', base_url)
            config_request['config']['name'] = name
            test_case_list[0] = config_request
        else:
            id = test_info[0]
            pre_request = eval(TestCase.objects(id=ObjectId(id)).first()['request'])
            test_case_list.append(pre_request)

    if request['test']['request']['url'] != '':
        test_case_list.append(request)

    dump_yaml_file(os.path.join(testcase_dir_path, name + '.yml'), test_case_list)


def run_by_suite(index, base_url, path):
    obj = TestSuite.objects(id=ObjectId(index)).first()

    include = eval(obj['include'])

    for val in include:
        run_by_single(val[0], base_url, path)


def run_by_batch(test_list, base_url, path, type=None, mode=False):
    """
    批量组装用例数据
    :param test_list:
    :param base_url: str: 环境地址
    :param type: str：用例级别
    :param mode: boolean：True 同步 False: 异步
    :return: list
    """

    if mode:
        for index in range(len(test_list) - 2):
            form_test = test_list[index].split('=')
            value = form_test[1]
            if type == 'project':
                run_by_project(value, base_url, path)
            elif type == 'module':
                run_by_module(value, base_url, path)
            elif type == 'suite':
                run_by_suite(value, base_url, path)
            else:
                run_by_single(value, base_url, path)

    else:
        if type == 'project':
            for value in test_list.values():
                run_by_project(value, base_url, path)

        elif type == 'module':
            for value in test_list.values():
                run_by_module(value, base_url, path)
        elif type == 'suite':
            for value in test_list.values():
                run_by_suite(value, base_url, path)

        else:
            for index in range(len(test_list) - 1):
                form_test = test_list[index].split('=')
                index = form_test[1]
                run_by_single(index, base_url, path)


def run_by_module(id, base_url, path):
    """
    组装模块用例
    :param id: int or str：模块索引
    :param base_url: str：环境地址
    :return: list
    """
    use_case_list = TestCase.objects(belongModuleId=ObjectId(id), configType=1)

    for use_case in use_case_list:
        run_by_single(use_case['_id'], base_url, path)


def run_by_project(id, base_url, path):
    """
    组装项目用例
    :param id: int or str：项目索引
    :param base_url: 环境地址
    :return: list
    """
    module_list = Module.objects(belongProjectId=ObjectId(id))
    for module in module_list:
        run_by_module(module['_id'], base_url, path)


def run_test_by_type(id, base_url, path, type):
    if type == 'project':
        run_by_project(id, base_url, path)
    elif type == 'module':
        run_by_module(id, base_url, path)
    elif type == 'suite':
        run_by_suite(id, base_url, path)
    else:
        run_by_single(id, base_url, path)
