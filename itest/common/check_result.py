# encoding: utf-8
"""
@author: han.li
@file  : check_result.py
@time  : 11/22/18 10:52 AM
@dec   : 结果检查类
"""

import re
from itest.utils.compares import get_eqs_json, get_contain_json, get_eqs_str, get_contain_str

class CheckResult(object):
    """
    结果比对类
    check_rule {
                check_field:'', #  检查字段： 1 默认 响应文本（resp） ， 2 响应代码(resp.status_code)， 3 响应信息(resp.text)，
                                    4 相应头(resp.headers)
                rule:'',  # assert rule 判断规则 ：
                    1 包括（include） 返回结果包含 指定的内容， 支持正则表达式  默认
                    2 匹配（equals） 指符合结果与指定的内容 完全一致
                    3 后续在加
                }
    """
    def __init__(self, source_data, expect_data, check_rule):
        self.source_data = source_data
        self.expect_data = expect_data
        self.check_rule = check_rule
        self.data = None
        self.type = 'str'
        self.set_data_and_type()
        self.result = {
            'success': True,
            'error':"",
            'data': {}
        }

    def set_result(self, success, ):
        if success:
            self.result = {
                'success' : True,
                'error': '',
                'data': {'src_data':self.data, 'expect_data':self.expect_data}
            }
        else:
            self.result = {
                'success': False,
                'error': '', # 失败详情
                'data': {'src_data':self.data, 'expect_data':self.expect_data}
            }

    def get_result(self):
        return self.result

    def compare(self):
        if self.type == 'json':
            if self.check_rule['rule'] == "include":
                return get_contain_json(self.data, self.expect_data)
            elif self.check_rule['rule'] == "equals":
                return get_eqs_json(self.data, self.expect_data)
        elif self.type == 'str':
            if self.check_rule['rule'] == "include":
                return get_contain_str(str(self.data), str(self.expect_data))
            elif self.check_rule['rule'] == "equals":
                return get_eqs_str(str(self.data), str(self.expect_data))

    def set_data_and_type(self):
        check_field = self.check_rule.get('checkField')
        if check_field == 'resp':
            self.data = self.source_data
            self.type = 'json'
        elif check_field == 'resp.status_code':
            self.data = self.source_data.status_code
            self.type = 'str'
            result = self.compare(self.source_data['status_code'], 'str')
        elif check_field == 'resp.text':
            self.data = self.source_data.text
            self.type = 'json'
        elif check_field == 'headers':
            self.data = self.source_data.headers
            self.type = 'str'

    def check(self):
        if self.data:
            result = self.compare()
            self.set_result(result)
        else:
            self.result = {
                'success' : False,
                'error':'not find %s' % self.check_rule['check_field'],
                'data': {'src_data':self.source_data, 'expect_data':self.expect_data}
            }

    def check_detail(self):
        if self.check_rule['rule'] == "include":
            check_str = self.get_str_by_check_field()
            check = re.match(str(self.expect_data), check_str,flags=0)
            if check:
                CheckResult = {
                    'passed': True,
                    'error': '',
                    'error_detail': {}
                }
            else:
                CheckResult = {
                    'passed': False,
                    'error': '结果校验失败',
                    'errorDetail': {
                        'check_rule': self.check_rule,
                        'check_data': self.source_data,
                        'expect_data': self.expect_data
                    }
                }
        elif self.check_rule['rule'] == 'equals':
            return True





