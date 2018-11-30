# encoding: utf-8
"""
@author: han.li
@file  : s_interface_use_case.py
@time  : 11/5/18 2:05 PM
@dec   : 接口用例管理服务
"""



from itest.model.m_interface_use_case import InterfaceUseCase
from itest.model.m_interface_use_case_execution import InterfaceUseCaseExecution
from itest.service.image.s_image import ImageService
from itest.common.use_case_request import UseCaseRequest
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from mongoengine.errors import NotUniqueError
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id
from requests import Response

class InterfaceUseCaseService(object):
    def __init__(self):
        pass

    @staticmethod
    def execute_use_case(use_case_id):
        use_case = InterfaceUseCaseService.get_by_id(use_case_id)
        # 上传文件 本地转换
        if use_case['option']['requestType'] == 2:
            true_files = {}
            # 缓存图片id
            for key, value in use_case['option']['files'].items():
                image = ImageService.get_by_id(value)
                if not image:
                    return {
                            'status': 5000,
                            'data': {},
                            'costTime': 100
                        }, {
                            'passed': False,
                            'error': "获取图片失败异常",
                            'errorDetail': {}
                        }
                else:
                    true_files[key] = (image['name'], open(image['path'], 'rb'), 'multipart/form-data')
            use_case['option']['files'] = true_files

        ucr = UseCaseRequest(use_case)
        ucr.run()
        result = ucr.get_result()
        if isinstance(result['response']['data'], Response):
            response = {
                'status_code': result['response']['data'].status_code,
                'text': result['response']['data'].text,
                'headers': result['response']['data'].headers
            }
            result['response']['data'] = response
        print(result['response'], result['expectResult'])
        return result['response'], result['expectResult']



    @staticmethod
    def create(use_case):
        creator_id = get_user_id()
        status = 'ok'
        try:
            rs = InterfaceUseCase(name=use_case['name'],
                                  interfaceId=ObjectId(use_case['interfaceId']),
                                  environmentId=ObjectId(use_case['environmentId']),
                                  creatorId=ObjectId(creator_id),
                                  groupId=ObjectId(use_case['groupId']),
                                  level=use_case['level'],
                                  useCaseNo=use_case['useCaseNo'],
                                  detail=use_case['detail'],
                                  option=use_case['option'],
                                  projectId=ObjectId(use_case['projectId']),
                                  desc=use_case['desc']).save()
        except InvalidId:
            rs = None
            status = 'not_object_id'
        except NotUniqueError:
            rs = None
            status = 'not_unique'
        return convert_mongo_to_json(rs), status

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(InterfaceUseCase.objects(name=name).first())

    @staticmethod
    def get_by_id(use_case_id):
        return convert_mongo_to_json(InterfaceUseCase.objects(id=ObjectId(use_case_id), isDeleted=False).first())

    @staticmethod
    def get_by_id_list(id_list):
        return convert_queryset_to_json(InterfaceUseCase.objects(id__in=id_list, isDeleted=False))

    @staticmethod
    def get_use_cases(project_id):
        status = 'ok'
        try:
            rs = InterfaceUseCase.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_queryset_to_json(rs), status

    @staticmethod
    def find(q, project_id):
        """
        模糊查询
        :return:
        """
        return convert_queryset_to_json(InterfaceUseCase.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q)) & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime"))

    @staticmethod
    def update(use_case):
        status = 'ok'
        try:
            data = InterfaceUseCase.objects(id=ObjectId(use_case['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=use_case['name'],
                             desc=use_case['desc'],
                             interfaceId=ObjectId(use_case['interfaceId']),
                             environmentId=ObjectId(use_case['environmentId']),
                             groupId=ObjectId(use_case['groupId']),
                             level=use_case['level'],
                             useCaseNo=use_case['useCaseNo'],
                             detail=use_case['detail'],
                             option=use_case['option'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        except NotUniqueError:
            rs = None
            status = 'not_unique'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(use_case):
        status = 'ok'
        try:
            data = InterfaceUseCase.objects(id=ObjectId(use_case), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + use_case
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status
