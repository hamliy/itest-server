#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 lihan
# @Time    : 2019/1/13 上午10:02
# @Author  : lihan
# @File    : db_operation.py
# @Dec     : 数据库操作

from pymongo import MongoClient
from datetime import datetime
from itest.tools.train_info.util import getMonthFirstDayAndLastDay

MONGO_URL = 'mongodb://172.20.166.50:27017/'
DB_NAME = 'train'

def get_set(dbset):
    """
    获取表
    :param dbset:
    :return:
    """
    md = MongoClient(MONGO_URL)
    db = md[DB_NAME]
    return db[dbset]

def get_station_code_order_by_name():
    """
    根据获取车站名及对应编号
    :param station_name:
    :return:
    """
    set = get_set('train_station')
    year = datetime.utcnow().year  # 当前月份
    month = datetime.utcnow().month  # 当前月份
    fist_day, last_day = getMonthFirstDayAndLastDay(year, month)
    all_station = set.find({'createTime':{ "$gte" : fist_day, "$lt" : last_day }})
    result = {}
    for station in all_station:
        result[station['stationName']] = station['stationCode']
    return result
def update_train_info(data):
    """
    更新车次库
    :return:
    """
    set = get_set('train_info')
    set.insert_one(data)
    # data = {
    #     'number': '',
    #     'start': '',
    #     'start_time': '',
    #     'end': '',
    #     'end_time': '',
    #     'price': '',
    #     'cost_time': '',
    #     'seat': {'type': 'price', '': ''}
    # }
    # all = set.find({'name': number})
    # for one in all:
    #     print(one)

