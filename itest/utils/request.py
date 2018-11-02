#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018 lihan
# @Time    : 2018/9/2 下午4:16
# @Author  : lihan
# @File    : request.py
# @Dec     : 

"""
    接口请求通用方法集
"""
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse
from posixpath import normpath


# url+api拼接
def uri_join(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

