# encoding: utf-8
"""
@author: han.li
@file  : utils.py
@time  : 8/28/18 9:23 PM
@dec   : 
"""
import json, os, time, io, yaml
import datetime
from bson import ObjectId
import hashlib

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
    if not queryset:
        return data
    for item in queryset:
        data.append(convert_mongo_to_json(item))
    return data


# 获取项目路径
def get_project_path():
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(utils_dir, ".."))


# 获取用例执行目录
def get_test_dir():
    return os.path.join(get_project_path(), 'test_case_dir')


# 获取用例执行路径
def get_test_dir_path(type):
    path = os.path.join(get_test_dir(), type)
    return os.path.join(path, get_time_stamp())


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


# httprunner 运行结果时间戳格式转换
def timestamp_to_datetime(summary, type=True):
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime.datetime. \
            fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary

# 获取当前时间戳
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H-%M-%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs)
    return time_stamp


def dump_yaml_file(yaml_file, data):
    """ load yaml file and check file content format
    """
    with io.open(yaml_file, 'w', encoding='utf-8') as stream:
        yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8')


def _dump_json_file(json_file, data):
    """ load json file and check file content format
    """
    with io.open(json_file, 'w', encoding='utf-8') as stream:
        json.dump(data, stream, indent=4, separators=(',', ': '), ensure_ascii=False)


def dump_python_file(python_file, data):
    with io.open(python_file, 'w', encoding='utf-8') as stream:
        stream.write(data)

