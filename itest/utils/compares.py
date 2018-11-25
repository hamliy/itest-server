#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/11/25 下午6:51
# @Author  : lihan
# @File    : compares.py
# @Dec     : 比较通用方法

from jsondiff import diff
from jsondiff.symbols import Symbol
import re

# 比较json是否相等
def get_eqs_json(src_data, dst_data):
    if diff(src_data, dst_data) == {}:
        return True
    else:
        return False


# 比较字典 是否包含 src 包含 dst
def get_contain_json(src_data, dst_data):
    return diff_just_delete(diff(src_data, dst_data))


# 判断 diff结果是否只是缺少的数据， 来匹配包含
def diff_just_delete(differ):
    for key, value in differ.items():
        if isinstance(key, Symbol):
            if str(key) != '$delete':
                return False
        else:
            if isinstance(value, dict) and value:
                if not diff_just_delete(value):
                    return False
            else:
                return False
    return True

# 比较字符串是否相等
def get_eqs_str(src_data, dst_data):
    if dst_data == src_data:
        return True
    else:
        return False


# 比较字符串 是否包含 src 包含 dst
def get_contain_str(src_data, dst_data):
    if re.search(dst_data, src_data):
        return True
    else:
        return False
