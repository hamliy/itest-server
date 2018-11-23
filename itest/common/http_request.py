# encoding: utf-8
"""
@author: han.li
@file  : http_request.py
@time  : 11/21/18 2:45 PM
@dec   : http请求封装
"""

import time
import requests


# 响应时间统计装饰器
def time_statistics(origin_func):
    def wrapper(self, *args, **kwargs):
        start = time.time()
        try:
            u = origin_func(self, *args, **kwargs)
        except Exception as e:
            self.cost_time = round(time.time() - start, 2)
            status = 0
            error = "Raise an exception  %s" % self.params
            self.set_response(data=str(e), status=status, error=error)

            return 'error'
        self.cost_time = round(time.time() - start, 2)
        return u
    return wrapper


class HttpRequest(object):
    """
        通用用例实例模板
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
            'method': 'POST',
            'params': {},
            'data': {},
            'files': {},
            'request_type': 0
        }
        # 接口请求耗时
        self.cost_time = 0
        # 接口返回值地那样
        self.response = {
            'cost_time': 0,
            'status': 1,  # 0 失败 1 成功
            'error_info': '',
            'data': {}
        }
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.method = 'GET'
        self.request_type = 0  # post => json ,file, params
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
        self.method = self.request['method']
        self.request_type = self.request['request_type']

    def request_run(self):
        method = self.method.upper()
        if method == "GET":
            self.get()
        elif method == "POST":
            self.post()
        else:
            self.set_response({'method': self.method}, status=0, error='Please set request type post or get')

    def get_response(self):
        return self.response

    def set_response(self, data={}, status=1, error=''):
        self.response['status'] = status
        self.response['error_info'] = error
        self.response['data'] = data
        self.response['cost_time'] = self.cost_time

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

        # 请求异常不是200
        # 请求异常
        if resp is None:
            self.set_response(data=resp, status=5001, error="response was None !")
            return
        # if resp is None or resp.status_code != 200:
        #     status = 0
        #     if resp is None:
        #         error = "response was None !"
        #         data = resp
        #     else:
        #         error = "status_code == %s not 200" % resp.status_code
        #         data = resp.text
        #     self.set_response(data=data, status=status, error=error)
        #     return

        self.set_response(resp)

    def post(self):
        """
        defined post method
        :return:
        """
        if self.request_type == 0:
            resp = self.post_with_normal()
        elif self.request_type == 1:
            resp = self.post_with_json()
        else:
            resp = self.post_with_file()

        if resp == 'error':
            return
        # 请求异常
        if resp is None:
            self.set_response(data=resp, status=5001, error="response was None !")
            return
        # if resp is None or resp.status_code != 200:
        #     status = 0
        #     if resp is None:
        #         error = "response was None !"
        #         data = resp
        #     else:
        #         error = "status_code == %s not 200" % resp.status_code
        #         data = resp.text
        #     self.set_response(data=data, status=status, error=error)
        #     return
        data = resp
        self.set_response(data)

    @time_statistics
    def get_with_normal(self):
        """
        defined post method
        :return:
        """
        return requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))


    # defined http post method
    # include get params and post data
    # uninclude upload file
    @time_statistics
    def post_with_normal(self):
        """
        defined post method
        :return:
        """
        return requests.post(self.url, headers=self.headers, params=self.params, data=self.data,
                             timeout=float(timeout))


    # defined http post method
    # include upload file
    @time_statistics
    def post_with_file(self):
        """
        defined post method
        :return:
        """
        return requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                             timeout=float(timeout))


    # defined http post method
    # for json
    @time_statistics
    def post_with_json(self):
        """
        defined post method
        :return:
        """
        print(self.data)
        print(self.url)
        return requests.post(self.url, headers=self.headers, params=self.params, json=self.data, timeout=float(timeout))

