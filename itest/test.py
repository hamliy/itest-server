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
    headers ={'Content-Type': 'application/json'}
    res =requests.post(url="https://finchain.kchaintest.kingdeeresearch.com/api/user/login", headers=headers,params={},
                  json={'username': '17077187768', 'password': 'kingdee'}, timeout=float(60))
    print(res.text)


    # print(g.id)
    # print(celery_client.AsyncResult('6fc067b1-9581-416d-96b8-fda7276c2186').get())
