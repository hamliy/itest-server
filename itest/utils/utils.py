# encoding: utf-8
"""
@author: han.li
@file  : utils.py
@time  : 8/28/18 9:23 PM
@dec   : 
"""
import json
import datetime
from bson import ObjectId

from mongoengine.base import BaseDocument


def init_return(data, sucess=True, errorCode=100, error=''):
    return {
        "errorCode": errorCode,
        "success": sucess,
        "error": error,
        "data": data
    }


# mongo数据转字典
def mongo_to_dict(mongo_data):
    data = mongo_data.to_json()
    data = json.loads(data)
    return data


def get_value(src, key, init=''):
    # 获取对象value
    if key in src:
        return src[key]
    else:
        return init


# 使json能够转化datetime对象
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# 将 MongoDB 的 document转化为json形式
def convert_mongo_to_json(o):
    def convert(dic_data):
        # 对于引用的ID和该条数据的ID， 这里都是ObjectId类型
        # 字典遍历
        for key, value in dic_data.items():
            if isinstance(value, list):
                for l in value:
                    convert(l)
            else:
                if isinstance(value, ObjectId):
                    dic_data[key] = str(dic_data.pop(key))
        return dic_data

    ret = {}
    if isinstance(o, BaseDocument):
        # 转换为son形式
        data = o.to_mongo()
        # 转化为字典
        data = data.to_dict()
        ret = convert(data)
    # 将数据转化为json格式， 因json不能直接处理datetime类型的数据， 故需要区分处理
    # ret = json.dumps(ret, cls=DateEncoder)
    # ret = json.loads(ret)
    return ret

