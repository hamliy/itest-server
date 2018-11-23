# encoding: utf-8
"""
@author: han.li
@file  : utils.py
@time  : 8/28/18 9:23 PM
@dec   : 
"""
import json, os
import datetime
from bson import ObjectId
import hashlib
import operator
from jsondiff import diff
from jsondiff.symbols import Symbol

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
                    if isinstance(l, dict):
                        convert(l)
            else:
                # 转换id
                if isinstance(value, ObjectId):
                    # temp = str(dic_data.pop(key))
                    dic_data[key] = str(value)
                # 转换日期格式
                if isinstance(value, datetime.datetime):
                    dic_data[key] = (value + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, datetime.date):
                    dic_data[key] = value.strftime("%Y-%m-%d")
        return dic_data

    ret = {}
    if isinstance(o, BaseDocument):
        # 转换为son形式
        data = o.to_mongo()
        # 转化为字典
        data = data.to_dict()
        ret = convert(data)
    # 默认删除isDeleted字段
    if 'isDeleted' in ret:
        ret.pop('isDeleted')
    # _id 转换为 id
    if '_id' in ret:
        ret['id'] = ret.pop('_id')
    return ret


# mongo 查询结果集转json
def convert_queryset_to_json(queryset):
    data = []
    for item in queryset:
        data.append(convert_mongo_to_json(item))
    return data

# 获取项目路径
def get_project_path ():
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(utils_dir, ".."))


# 获取项目静态图像路径
def get_images_path ():
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(utils_dir, "../../../static/test_data/images/"))


# md5 加密
def md5(str):
    # 创建md5对象
    m = hashlib.md5()
    b = str.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()


# 比较json是否相等
def get_cmp_json(src_data, dst_data):
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
