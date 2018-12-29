# encoding: utf-8
"""
@author: han.li
@file  : use_case_request.py
@time  : 11/21/18 2:45 PM
@dec   : 用例请求封装
"""
import datetime
from itest.common.api_request import ApiRequest
from itest.utils.request import uri_join, get_use_case_url
from itest.common.check_result import CheckResult


def getKeyValue(objs):
    """
    获取key value
    :return:
    """
    obj = {}
    for item in objs:
        obj[item['key']] = item['example']
    return obj


class UseCaseRequest(ApiRequest):
    def __init__(self, use_case, env):
        self.use_case = use_case
        self.env = env
        request = self.init_use_case_request()
        super(UseCaseRequest, self).__init__(request)
        self.case_name = use_case['name']
        self.expect = use_case['options']['expect']
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
        options = self.use_case['options']
        url = get_use_case_url(self.env['protocol'], self.env['ip'],
                               self.env['port'], options['path'])
        request_params = {
            'url': url,
            'headers': getKeyValue(options['headers']['params']),
            'method': options['method'],
            'params': {},
            'data': {},
            'json': {},
            'files': None,
            'requestType': 'get'
        }
        data = options['data']['params']
        # 按参数请求
        if options['type'] == 'query':
            request_params['params'] = getKeyValue(data['query'])
        # 根据headers content-type 判断
        elif options['type'] == 'json':
            request_params['json'] = getKeyValue(data['json'])
        elif options['type'] == 'form':
            request_params['data'] = getKeyValue(data['form'])
        elif options['type'] == 'path':
            item = getKeyValue(data['path'])
            for key, value in item.getItems():
                request_params['url'] += '/'+value
        return request_params

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
