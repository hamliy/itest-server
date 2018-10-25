# encoding: utf-8
"""
@author: han.li
@file  : models.py
@time  : 8/15/18 3:25 PM
@dec   : 
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField, FloatField, IntField, DictField,
    ListField, ReferenceField, StringField, ObjectIdField, BooleanField
)
import json, logging
from mongoengine import signals

"""
    通用数据集合
    8 项目集合
    0 接口集合
    1-1 接口参数数据
    1 接口请求数据
    2 接口返回值数据
    3 用例集合
    4 用例执行记录集合
    5 任务集合
    6 环境集合
    7 更新数据
"""

def handler(event):
    """Signal decorator to allow use of callback functions as class decorators."""

    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator


# 创建初始化创建时间
@handler(signals.pre_save)
def init_create_info(sender, document, **kwargs):
    document.create_info = OperatorInfo(username='admin', time=datetime.utcnow())


class OperatorInfo(EmbeddedDocument):
    """7 更新数据修改人 时间"""

    username = StringField()                # 操作人员
    time = DateTimeField()                  # 更新时间

@init_create_info.apply
class Project(Document):
    """
    8 项目集合
    项目 关联 1、用例、任务、环境信息
    """
    meta = {'collection': 'project'}

    name = StringField()                                # 项目名
    version = StringField()                             # 项目版本号 V1.0 后续创建版本管理
    type = StringField()                                # 项目类型   Web， app
    description = StringField()                         # 备注信息
    update_info = EmbeddedDocumentField(OperatorInfo)   # 更新记录
    create_info = EmbeddedDocumentField(OperatorInfo)   # 创建记录

    def to_dict(self):
        data = self.to_json()
        data = json.loads(data)
        # data['id'] = data["_auto_id_0"]['$oid']
        # data.pop('_auto_id_0')
        return data


class HeaderParamPairs(EmbeddedDocument):
    """0-1 接口请求参数数据对"""
    name = StringField()                     # 参数名
    value = StringField()               # 参数值
    required = BooleanField()               # 是否必需
    example = StringField()             # 示例
    desc = StringField()             # 说明


class RequestParamPairs(EmbeddedDocument):
    """0-1 接口请求参数数据对"""
    name = StringField()                     # 参数名
    param_type = StringField()               # 类型
    required = BooleanField()                # 是否必需
    example = StringField()  # 示例
    desc = StringField()             # 说明


class ResponseParamPairs(EmbeddedDocument):
    """0-1 接口返回参数数据对"""
    name = StringField()                        # 参数名
    param_type = StringField()                  # 类型
    required = BooleanField()                   # 是否必需
    default = BooleanField()                   # 默认值
    desc = StringField()                        # 说明

@init_create_info.apply
class Interface(Document):
    """0 接口集合"""
    meta = {'collection': 'interface'}

    project_id = ReferenceField(Project, required=True)       # 所属项目
    name = StringField(required=True)                    # 接口名
    path = StringField(required=True)               # 接口
    method = StringField(default='GET', required=True)                    # 接口请求类型 post get
    content_type = StringField(default='')            # 接口数据类型
    req_body_type = StringField(default='json')                                        # 接口请求参数类型：form json file raw
    req_body_params = ListField(EmbeddedDocumentField(RequestParamPairs), default=[])       # 接口请求参数定义
    res_body_type = StringField(default='json')                                        # 返回结果类型 json raw
    req_example = StringField(default='')                                             # 接口请求示例
    res_body_params = ListField(EmbeddedDocumentField(ResponseParamPairs), default=[])       # 接口返回结果参数定义
    res_example = StringField(default='')                                                     # 接口返回示例
    headers = ListField(EmbeddedDocumentField(HeaderParamPairs), default=[])                  # 接口头文件
    desc = StringField(default='')                                          # 接口备注
    update_info = EmbeddedDocumentField(OperatorInfo) # 更新记录
    create_info = EmbeddedDocumentField(OperatorInfo) # 创建记录


class ApiRequest(EmbeddedDocument):
    """1 接口请求数据"""
    name = StringField()                    # 接口名
    uri = StringField()                     # 请求路径
    type = StringField()                    # 请求类型
    content_type = StringField()            # 请求格式
    headers = DictField()                   # 请求头文件
    params = DictField()                    # 请求参数
    data = DictField()                      # 请求数据
    files = DictField()                     # 请求文件
    remarks = DictField()                   # 请求备注


class ApiResponse(EmbeddedDocument):
    """2 接口返回值数据"""
    cost_time = FloatField()                # 请求耗时
    success = BooleanField()                # 请求结果状态 True 成功 False 失败
    error_code = IntField()                 # 请求失败错误码 100 成功， 其他失败
    error = StringField()                   # 失败信息
    data = StringField()                    # 请求返回结果

    def to_dict(self):
        data = self.to_json()
        data = json.loads(data)
        return data


class UseCaseParams(EmbeddedDocument):
    """请求参数"""

    key = StringField()
    value = StringField()
    description = StringField()


class UseCaseRequest(EmbeddedDocument):
    """用例请求信息"""

    headers = ListField(EmbeddedDocumentField(HeaderParamPairs))  # 请求头
    interface_path = StringField()                          # 请求接口路径
    request_type = StringField()
    interface = ReferenceField(Interface)                   # 关联接口


@init_create_info.apply
class UseCase(Document):
    """3 用例集合"""
    meta = {'collection': 'use_case'}

    project = ReferenceField(Project)                               # 所属项目
    name = StringField()                                            # 用例名
    request = EmbeddedDocumentField(UseCaseRequest)                 # 用例接口请求信息
    params = ListField(EmbeddedDocumentField(UseCaseParams))        # 用例请求参数
    expect = DictField()                                            # 用例预期结果
    rule = DictField()                                              # 预期结果校验规则
    update_info = EmbeddedDocumentField(OperatorInfo)               # 更新记录
    create_info = EmbeddedDocumentField(OperatorInfo)               # 创建记录
    remarks = DictField()                                           # 用例备注
    # 运行用例
    def invoke_use_case(self, task=None, envoriment_url=''):
        use_case = self
        response = ApiResponse(cost_time=1, success=True, error_code=100, error='', data="{'fphm':'test_fphm'}")
        status = 0,
        source_type = 'task'
        source_data = task
        environment_url = envoriment_url
        remarks = {'data':'invoke success'}
        InvokeUsecase(use_case=use_case, response=response,source_type=source_type,
                      environment_url=environment_url,
                      source_data=source_data, status=status[0], remarks=remarks).save()

@init_create_info.apply
class Environment(Document):
    """6 环境集合"""
    meta = {'collection': 'environment'}

    project = ReferenceField(Project)   # 所属项目
    name = StringField()                # 环境名
    value = StringField()               # 环境url ip+port
    type = StringField()                # 类型 env variable
    description = StringField()         # 环境备注
    update_info = EmbeddedDocumentField(OperatorInfo) # 更新记录
    create_info = EmbeddedDocumentField(OperatorInfo) # 创建记录


class InterfaceNode(EmbeddedDocument):
    """1 接口主题节点数据数据"""
    interface_id = ReferenceField(Interface)    # 所属接口
    name = StringField()                        # 名称
    desc = StringField()                        # 描述


class ThemeNode(EmbeddedDocument):
    """1 接口主题节点数据数据"""
    list = ListField(EmbeddedDocumentField(InterfaceNode))     # 子节点
    name = StringField()                    # 名称
    desc = StringField()             # 描述

class Theme(Document):
    """7 接口主题集合--两层结构"""
    meta = {'collection': 'interface_theme'}

    project_id = ReferenceField(Project)   # 所属项目
    name = StringField()                # 主题名
    desc = StringField()         # 备注
    list = ListField(EmbeddedDocumentField(InterfaceNode))              # 子节点
    sub_themes = ListField(EmbeddedDocumentField(ThemeNode))


class TaskUseCase(EmbeddedDocument):
    """任务对应的用例"""

    use_case_id = ObjectIdField()                       # 用例对应id
    use_case_name = StringField()                       # 用例名
    use_case_request = EmbeddedDocumentField(UseCaseRequest)               # 用例接口请求信息
    rule = DictField()                                  # 预期结果校验规则
    params = DictField()                                # 用例参数
    expect = DictField()                                # 用例预期结果
    status = IntField()                                 # 用例执行结果 0 成功 1 失败 2 异常
    invoke_detail = ObjectIdField()                     # 用例执行情况


class InvokeUsecase(Document):
    """4 用例执行记录集合"""

    meta = {'collection': 'invoke_use_case'}

    use_case = EmbeddedDocumentField(TaskUseCase)   # 执行对应用例
    response = EmbeddedDocumentField(ApiResponse)   # 接口请求
    environment_url = StringField()                 # 环境url
    status = IntField()                             # 用例执行结果 3 未执行 0 成功 1 失败 2 异常
    source_type = StringField()                     # 执行用例来源类型 task 任务
    source_data = StringField()                     # 来源数据  task对应
    remarks = DictField()                           # 备注信息

class TaskEnvironment(EmbeddedDocument):
    """任务对应环境信息"""

    url = StringField()                                 # 环境地址
    environment = ReferenceField(Environment)           # 环境信息


@init_create_info.apply
class Task(Document):
    """5 任务集合"""
    meta = {'collection': 'task'}

    project = ObjectIdField()                               # 所属项目
    name = StringField()                                    # 任务名
    environment = EmbeddedDocumentField(TaskEnvironment)               # 环境信息
    use_cases = ListField(EmbeddedDocumentField(TaskUseCase))          # 用例集合
    status = IntField()                                     # 任务执行状态 0 未执行 1 执行中 2 已完成
    update_info = EmbeddedDocumentField(OperatorInfo)       # 更新记录
    create_info = EmbeddedDocumentField(OperatorInfo)       # 创建记录
    remarks = DictField()                                   # 备注信息
    summary = DictField()                                   # 任务综述

    # 运行任务
    def run_task(self):
        task = self
        environment_url = self.environment.url
        for use_case in self.use_cases:
            self.invoke_use_case(use_case, environment_url)
        self.update_status

    # 运行用例
    def invoke_use_case(self, use_case, environment_url=''):

        response = ApiResponse(cost_time=1, success=True, error_code=100, error='', data="{'fphm':'test_fphm'}")
        status = 0,
        source_type = 'task'
        source_data = self.id
        environment_url = environment_url
        remarks = {'data':'invoke success'}
        InvokeUsecase(use_case=use_case, response=response,source_type=source_type,
                      environment_url=environment_url,
                      source_data=source_data, status=status[0], remarks=remarks).save()

    # 更新任务状态
    def update_status(self):
        total = len(self.use_cases)
        InvokeUsecase
        pass

