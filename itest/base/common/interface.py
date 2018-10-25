# encoding: utf-8
"""
@author: han.li
@file  : interface.py
@time  : 10/15/18 2:42 PM
@dec   : 接口调用方法
"""
from bson import ObjectId
from itest.models import Interface
from itest.utils.utils import init_return


class BaseInfo(object):
    """
    基本信息类： 项目id， 名字，描述
    """
    def __init__(self, project_id, name, mongo_cls):
        self.project_id = project_id
        self.name = name
        self.mongo_cls = mongo_cls

    def get_data(self):
        # 根据项目id和名称获取数据库信息
        return self.mongo_cls.objects(name=self.name, project_id=ObjectId(self.project_id)).first()

    def check_existed(self):
        if self.get_data() is None:
            return True
        else:
            return False


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

    @staticmethod
    def get_interface(interface_id):
        return Interface.objects(id=ObjectId(interface_id))
    # 保存入库
    def save(self):
        if self.check_existed():
            api = self.mongo_cls(name=self.name, project_id=ObjectId(self.project_id),
                                 path=self.path, method=self.method, desc=self.desc).save()
            return init_return({'id': api.id})
        else:
            return init_return({}, sucess=False, error="存在相同接口名", errorCode=1001)

    # 更新数据
    def update(self):
        pass

    # 删除塑胶
    def remove(self):
        pass

    def get_first(self):
        # 获取数据库数据
        self.get_data()
