# encoding: utf-8
"""
@author: han.li
@file  : use_case_request.py
@time  : 11/21/18 2:45 PM
@dec   : 用例请求封装
"""
import datetime
import json
from itest.common.http_request import HttpRequest
from itest.utils.request import uri_join
from itest.service.image.s_image import ImageService

class UseCaseRequest(HttpRequest):
    def __init__(self, use_case):
        self.use_case = use_case
        request = self.init_use_case_request()
        super(UseCaseRequest, self).__init__(request)
        self.case_name = use_case['name']
        self.expected = use_case['option']['expect']
        self.check_rule = use_case['option']['checkRule']
        self.status = 1
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
            'request_type': option['request_type']
        }

    def run(self):
        run_time = datetime.datetime.utcnow
        self.request_run()
        self.is_run = True
        self.result['run_time'] = run_time
        self.result['case_name'] = self.case_name
        self.result['response'] = self.response
        self.result['request'] = self.request

        # self.check_expected()

        self.result['status'] = self.status
        self.result['expected'] = self.expected

    def check_expected(self):

        if 'data' in self.expected and self.expected['data']:
            response = self.response
            info = json.loads(response['data'])
            expected = self.expected['data']

            noerror = True
            if 'errorCode' in expected:
                if 'errorCode' in info:
                    if str(info['errorCode']) != str(expected['errorCode']):
                        noerror = False
                        self.expected['not_match'].append({
                            'name': 'errorCode',
                            'response': info['errorCode'],
                            'expected': expected['errorCode'],
                            'reason': 'Not Match'
                        })
                        self.status = 0
                else:
                    noerror = False
                    self.expected['not_match'].append({
                        'name': 'errorCode',
                        'response': '',
                        'expected': expected['errorCode'],
                        'reason': 'response not Found errorCode'
                    })
                    self.status = 0

            if noerror:
                if 'data' in response :
                    detail = json.loads(response['data'])
                    if detail is not None and 'data' in detail and detail['data'] is not None:
                        if 'data' in expected:
                            self.compare(detail['data'], expected['data'])
                    else:
                        self.status = 0
                else:
                    self.status = 0

    def compare(self, src_data, expected):
        not_match = []
        for key, value in expected.items():
            if key in src_data:
                if value != src_data[key]:
                    not_match.append({
                        'name': key,
                        'response': src_data[key],
                        'expected': value,
                        'reason': 'Not equal'
                    })
            else:
                not_match.append({
                    'name': key,
                    'response': '',
                    'expected': value,
                    'reason': 'Not Found'
                })
        if len(not_match) > 0:
            self.status = 0
        self.expected['not_match'] = not_match

    def get_result(self):
        return self.result
