# encoding: utf-8
"""
@author: han.li
@file  : check_result.py
@time  : 11/22/18 10:52 AM
@dec   : 结果检查类
"""

import re

class CheckResult(object):
    """
    结果比对类
    check_rule {
                check_field:'', #  检查字段： 1 默认 响应文本（resp） ， 2 响应代码(resp.status_code)， 3 响应信息(resp.text)，
                                    4 相应头(resp.headers)
                rule:'',  # assert rule 判断规则 ：
                    1 包括（include） 返回结果包含 指定的内容， 支持正则表达式  默认
                    2 匹配（equals） 指符合结果与指定的内容 完全一致
                    3 后续在叫
                }
    """
    def __init__(self, source_data, expect_data, check_rule):
        self.source_data = source_data,
        self.expect_data = expect_data
        self.check_rule = check_rule

    def get_str_by_check_field(self):
        check_field = self.check_rule['check_field']
        field = ""
        if check_field == 'resp':
            field = str(self.source_data)
        elif check_field == 'status_code' and 'status_code' in self.source_data:
            field = str(self.source_data['status_code'])
        elif check_field == 'text' and 'status_code' in self.source_data:
            field = str(self.source_data['text'])
        elif check_field == 'headers'and 'headers' in self.source_data:
            field = str(self.source_data['headers'])
        return field

    def check(self):
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





