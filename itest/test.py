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
    data = {'proxy': 'HWTjmPpEDaS7Re5n9ibmaYFzpvaMhgKhjyFiKo9pHViv', 'accessToken': '15458996845fc99549decf5d8e858cd5',
            'channelId': 'test', 'uid': 'test', 'tid': 'test', 'wxid': 'test', 'name': 'test', 'tname': 'test'}
    print(data, type(data))
    headers ={'Content-Type': 'application/json'}
    res =requests.post(url="http://123.207.7.95:31697/kbdus/registerByProxy", headers=headers, json=data, timeout=float(60))
    print(res.text)


    # print(g.id)
    # print(celery_client.AsyncResult('6fc067b1-9581-416d-96b8-fda7276c2186').get())
