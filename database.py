# encoding: utf-8
"""
@author: han.li
@file  : database.py
@time  : 8/15/18 3:25 PM
@dec   : 初始化数据
"""

from itest.models import Task, UseCase, InvokeUsecase, ApiResponse, ApiRequest, Interface, Environment, Project, OperatorInfo
from datetime import datetime
from mongoengine import connect

connect('itest', host='mongodb://172.20.166.50:27017/itest2')

def get_operator():
    username = 'admin'
    return OperatorInfo(username=username, time = datetime.utcnow())
def init_db():

    # 创建项目
    project_name = '测试项目2'
    project_version = 'V1.0'
    project_type = None
    project_remarks = {'data':'测试项目'}
    project = Project(name=project_name, type=project_type, version=project_version, remarks=project_remarks).save()

    Project.objects(id=project.id).update_one(name='测试项目2')
    Project.objects(id=project.id).update_one(update_info=get_operator())
    # 创建环境
    env_name = '测试环境1'
    env_url = 'http://localhost:8082'
    env_remarks = {'data':'测试环境'}
    env = Environment(name=env_name, project=project, url=env_url,remarks=env_remarks).save()

    # 创建接口
    interface_name = '测试接口1'
    interface = '/images/info'
    type = 'post'
    content_type = 'application/json'
    params = {'image_name': False , 'image_path':True}
    headers = {}
    remarks = {'data':'接口备注'}
    api = Interface(name=interface_name, project=project, interface=interface, type=type, content_type=content_type,
                   params=params, headers=headers, remarks=remarks).save()
    # 创建用例
    use_case_name = '测试用例1'
    use_case_api = api
    params = {'image_name':'test.png', 'image_path':'path/test.png'}
    expect = {'fphm':'test_fphm'}
    use_case = UseCase(name=use_case_name, project=project, interface=use_case_api, params=params, expect=expect).save()

    # 创建任务
    task_name = '测试任务1'
    use_case_list = [use_case]
    task_status = 0,
    task_environment = env
    task_summary = {'data':'任务备注'}
    task = Task(name=task_name,use_cases=use_case_list, project=project, environment=task_environment, status=task_status[0], summary=task_summary).save()
    task.run_task()

from bson import ObjectId
def test():
    project_id = '5b913c515f627dec531de718'
    use = Interface.objects(id=ObjectId(project_id))
    use.update_one(request_type='test')
    print(use.to_json())

def init_interface():
    return ''
if __name__ == '__main__':
    # init_db()
    # test()
    id = "5b91e7b45f627dfd0621e9fa"
    id = "5b91e7b45f627dfd0621e9fa"
    use_case = UseCase.objects(id=ObjectId(id))
    print(use_case)
    print(use_case.count())
