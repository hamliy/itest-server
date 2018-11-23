# encoding: utf-8
"""
@author: han.li
@file  : test.py
@time  : 11/19/18 7:43 PM
@dec   : 
"""
from itest.celery_tasks import add
from itest.celery_client import celery_client
from celery import group
import requests, json
if __name__ == '__main__':
    # g = group(add.s(i, i ) for i in range(10))()
    # g.save()
    # print(g.get())
    headers ={'Cookie': 'finance-chain=99E754D253E3E9BE3070D929011D031C; Path=/api; HttpOnly, finchain_login=9f9ccd957e4bd46efa8ba90fde4b96629158416953f3f8e00c565be4ff2e2726eb61e4b7e2a73628fab5a3714a6fd3db'}
    res =requests.post(url="https://finchain.kchaintest.kingdeeresearch.com/api/user/login", headers=headers, params=None,
                  json={'username': '17077187768', 'password': 'kingdee'},
                  files=None, timeout=float(60))
    print(res.text)
    # print(g.id)
    # print(celery_client.AsyncResult('6fc067b1-9581-416d-96b8-fda7276c2186').get())
