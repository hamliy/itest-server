# encoding: utf-8
"""
@author: han.li
@file  : model.py
@time  : 5/16/18 10:27 AM
@dec   : common model
"""

import time
import requests


def time_statistics(origin_func):
    def wrapper(self, *args, **kwargs):
        start = time.time()
        try:
            u = origin_func(self, *args, **kwargs)
        except Exception as e:
            self.cost_time = round(time.time() - start, 2)
            status = 0
            error = "Raise an exception  %s" % self.params
            data = str(e)
            self.set_result(reponse=data, status=status, error=error)

            return 'error'
        self.cost_time = round(time.time() - start, 2)
        return u
    return wrapper


class ApiRequest(object):
    """
        接口请求类
        定义接口请求方式
        用例请求返回值
        用例参数
        用例通用方法
        -- 接口请求 后续加装饰
    """
    def __init__(self, request_data):
        global timeout
        timeout = 60
        # 接口请求数据
        self.request = {
            'url': '',
            'headers': {},
            'type': 'POST',
            'params': {},
            'data': {},
            'files': {},
            'content_type': '',
            'dec': {}
        }
        # 接口请求耗时
        self.cost_time = 0
        # 接口返回值地那样
        self.result = {
            'cost_time': 0,
            'status': 1,  # 0 失败 1 成功
            'error_info': '',
            'response': {}
        }
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.type = 'GET'
        self.content_type = ''  # post => json ,file, params
        self.init_request(request_data)

    def init_request(self, request_data):

        for key, value in request_data.items():
            if key in self.request:
                self.request[key] = value

        self.headers = self.request['headers']
        self.params = self.request['params']
        self.data = self.request['data']
        self.url = self.request['url']
        self.files = self.request['files']
        self.type = self.request['type']
        self.content_type = self.request['content_type']

    def request_run(self):
        request_type = self.type.upper()
        if request_type == "GET":
            self.get()
        elif request_type == "POST":
            self.post()
        else:
            self.set_result({'type': self.type}, status=0, error='Please set request type correct')

    def get_result(self):
        return self.result

    def set_result(self, response={}, status=1, error=''):
        self.result['status'] = status
        self.result['error_info'] = error
        self.result['response'] = response
        self.result['cost_time'] = self.cost_time

    def set_content_type(self, content_type):
        """
        set content_type
        :param content_type: request  content_type
        :return:
        """
        self.content_type = content_type

    def set_url(self, url):
        """
        set url
        :param url: interface url
        :return:
        """
        self.url = url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, files):
        """
        set upload files
        :param files:
        :return:
        """
        self.files = files

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """

        resp = self.get_with_normal()

        if resp == 'error':
            return

        self.set_result(resp)

    def post(self):
        """
           defined post method
           :return:
           """
        if self.content_type == 'json':
            resp = self.post_with_json()
        elif self.content_type == 'file':
            resp = self.post_with_file()
        else:
            resp = self.post_with_normal()
        if resp == 'error':
            return
        self.set_result(resp)

    @time_statistics
    def get_with_normal(self):
        """
        defined post method
        :return:
        """
        return requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))

    @time_statistics
    def post_with_normal(self):
        """
        defined post method
        :return:
        """
        return requests.post(self.url, headers=self.headers, params=self.params, data=self.data,
                              timeout=float(timeout))

    @time_statistics
    def post_with_file(self):
        """
        defined post method
        :return:
        """
        return requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(timeout))

    @time_statistics
    def post_with_json(self):
        """
        defined post method
        :return:
        """
        return requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))



