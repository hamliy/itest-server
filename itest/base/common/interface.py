# encoding: utf-8
"""
@author: han.li
@file  : interface.py
@time  : 10/15/18 2:42 PM
@dec   : 接口调用方法
"""
from bson import ObjectId
from itest.models import Interface
from itest.utils.utils import init_return, mongo_to_dict


class BaseInfo(object):
    """
    基本信息类： 项目id， 名字，描述
    """
    def __init__(self, project_id, name, mongo_cls):
        self.project_id = project_id
        self.name = name
        self.mongo_cls = mongo_cls
        self.data = {}

    def get_data(self):
        # 根据项目id和名称获取数据库信息
        return self.mongo_cls.objects(name=self.name, project_id=ObjectId(self.project_id)).first()

    def check_existed(self):
        if self.get_data() is None:
            return True
        else:
            return False

    # 校验更新接口是否存在
    def update_check(self):
        existed = Interface.objects(name=self.name, project_id=ObjectId(self.project_id)).first()
        if existed and str(existed.id) != id:
            return False
        else:
            return True



class CInterface(BaseInfo):
    """
    接口调用类
    """
    # 依赖有项目id
    def __init__(self, project_id, name, path, desc='', method='GET'):
        BaseInfo.__init__(self, project_id, name, Interface)
        self.path = path
        self.method = method
        self.desc = desc
        self.req_body_type = 'form-data'
        self.res_body_type = 'json'
        self.headers = [{
            'name': 'Content-Type',
            'value': 'application/json;charset=utf-8',
            'required': True
        }]

    @staticmethod
    def get_interface(interface_id):
        return Interface.objects(id=ObjectId(interface_id))

    # 编辑基本信息 name method desc
    def update_basic(self, id):
        if self.update_check():
            interface = Interface.objects(id=ObjectId(id))
            # source = mongo_to_dict(interface.first())
            interface.update_one(set__name=self.name, set__path=self.path,
                                 set__method=self.method, set__desc=self.desc)
            # if self.name != source['name']:
            #     interface.update_one(name=self.name)
            # if self.path != source['path']:
            #     interface.update_one(path=self.path)
            # if self.method != source['method']:
            #     interface.update_one(method=self.method)
            # if self.desc != source['desc']:
            #     interface.update_one(desc=self.desc)

            return init_return({'data': '更新成功'})
        else:
            return init_return({}, sucess=False, error="存在相同接口名", errorCode=1001)

    # 编辑头文件
    @staticmethod
    def update_header(id, headers):
        interface = Interface.objects(id=ObjectId(id))
        interface.update_one(headers=headers)

    @staticmethod
    def update_req_params(id, params, req_body_type):
        interface = Interface.objects(id=ObjectId(id))
        interface.update_one(req_body_params=params)
        interface.update_one(req_body_type=req_body_type)

    @staticmethod
    def remove(id):
        result = Interface.objects(id=ObjectId(id)).delete()
        if result == 0:
            return init_return({}, sucess=False, error="删除的接口不存在", errorCode=1001)
        else:
            return init_return({'data': '删除成功'})

    # 保存入库
    def new_add(self):
        if self.check_existed():
            api = self.mongo_cls(name=self.name, project_id=ObjectId(self.project_id),
                                 path=self.path, method=self.method,
                                 req_body_type=self.req_body_type,
                                 res_body_type=self.res_body_type,
                                 headers=self.headers,
                                 desc=self.desc).save()
            return init_return({'id': api.id})
        else:
            return init_return({}, sucess=False, error="存在相同接口名", errorCode=1001)

    # 更新数据
    def update(self):
        pass

    # 删除塑胶
    def remove(self):
        pass

# mongo数据通用操作
class MInterface(object):
    def __init__(self):
        self.cls = Interface

    def remove(self, id):
        result = self.cls.objects(id=ObjectId(id)).delete()
        if result == 0:
            return init_return({}, sucess=False, error="删除的接口不存在", errorCode=1001)
        else:
            return init_return({'data': '删除成功'})