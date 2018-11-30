# encoding: utf-8
"""
@author: han.li
@file  : use_case_request.py
@time  : 11/21/18 2:45 PM
@dec   : 用例请求封装
"""
import datetime
from itest.common.http_request import HttpRequest
from itest.utils.request import uri_join
from itest.common.check_result import CheckResult


class UseCaseRequest(HttpRequest):
    def __init__(self, use_case):
        self.use_case = use_case
        request = self.init_use_case_request()
        super(UseCaseRequest, self).__init__(request)
        self.case_name = use_case['name']
        self.expect = use_case['option']['expect']
        self.expect_result = {
            'passed': True,
            'errorDetail': []  # 失败详情
        }
        self.is_run = False
        self.result = {}

    def init_use_case_request(self):
        """
        初始化 用例请求参数
        :return:
        """
        option = self.use_case['option']
        url = uri_join(option['url'], option['path'])

        return {
            'url': url,
            'headers': option['headers'],
            'method': option['method'],
            'params': option['params'],
            'data': option['data'],
            'files': option['files'],
            'requestType': option['requestType']
        }

    def run(self):
        run_time = datetime.datetime.utcnow
        self.request_run()
        self.is_run = True
        self.result['runTime'] = run_time
        self.result['caseName'] = self.case_name
        self.result['response'] = self.response
        self.result['request'] = self.request

        self.check_expect()

        self.result['expectResult'] = self.expect_result

    def check_expect(self):
        if self.response['status']:
            check_list = []
            for expect in self.expect:
                data = expect['data']
                check_rule = expect['checkRule']
                cr = CheckResult(self.response.get('data'), data, check_rule)
                cr.check()
                check_list.append(cr.get_result())
            for check in check_list:
                if not check['success']:
                    self.expect_result['passed'] = False
                    self.expect_result['errorDetail'].append(check)
        else:
            self.expect_result['passed'] = False
            self.expect_result['errorDetail'].append({
                'success': False,
                'error': self.response['errorInfo'],
                'data': {}
            })

    def get_result(self):
        return self.result
