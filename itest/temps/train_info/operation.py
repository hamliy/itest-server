# encoding: utf-8
"""
@author: han.li
@file  : operation.py
@time  : 1/11/19 9:34 AM
@dec   : 火车票获取方法类
"""
import requests

def get_train_number():
    """
    从 jt2345网站获取所有火车车次信息
    :return:
    """
    url = "http://www.jt2345.com/huoche/checi"
    resp = requests.get(url)
    print(resp.text)

if __name__ == '__main__':
    get_train_number()

