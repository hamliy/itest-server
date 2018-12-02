# encoding: utf-8
"""
@author: han.li
@file  : s_environment.py
@time  : 11/5/18 1:53 PM
@dec   : 环境类 环境信息 crud
"""


from itest.model.m_environment import Environment
from itest.utils.utils import convert_mongo_to_json, convert_queryset_to_json
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q
from datetime import datetime
from itest.utils.request import get_user_id
import subprocess


class EnvironmentService(object):
    def __init__(self):
        pass

    @staticmethod
    def check_status(url):
        """
        检查ping状态
        :return:
        """
        p = subprocess.Popen(['./itest/service/environment/ping.sh', url], stdout=subprocess.PIPE)
        result = p.stdout.read()
        if result == '1\n':
            status = 2
            # print i,record[i],'----ping failed----'
        else:
            status = 1
            # print i,record[i],'----ping success----'
        return status

    @staticmethod
    def create(env):
        creator_id = get_user_id()
        # status = EnvironmentService.check_status(env['path'])
        return convert_mongo_to_json(Environment(name=env['name'],
                                                 protocol=env['protocol'],
                                                 ip=env['ip'],
                                                 port=env['port'],
                                                 # status=status,
                                                 creatorId=ObjectId(creator_id),
                                                 projectId=ObjectId(env['projectId']),
                                                 desc=env['desc']).save())

    @staticmethod
    def get_by_name(name):
        return convert_mongo_to_json(Environment.objects(name=name).first())

    @staticmethod
    def get_by_id(env_id):
        return convert_mongo_to_json(Environment.objects(id=ObjectId(env_id), isDeleted=False).first())

    @staticmethod
    def get_envs(project_id):
        print(get_user_id())
        status = 'ok'
        try:
            rs = Environment.objects(projectId=ObjectId(project_id), isDeleted=False).order_by("-createTime")
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_queryset_to_json(rs), status

    @staticmethod
    def find(q, project_id, page, page_size):
        """
        模糊查询
        :return:
        """
        if not page:
            page = 1
        if not page_size:
            page_size = 10
        total = Environment.objects(projectId=ObjectId(project_id)).count()
        data = convert_queryset_to_json(Environment.objects(
            (Q(name__icontains=q) | Q(desc__icontains=q) | Q(ip__icontains=q))
            & Q(isDeleted=False) & Q(projectId=ObjectId(project_id)))
                                        .order_by("-createTime")[page_size * (page - 1):page_size * page])
        return {
            "total": total,
            "data": data
        }
    @staticmethod
    def update(env):
        status = 'ok'
        try:
            data = Environment.objects(id=ObjectId(env['id']), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            rs = data.modify(name=env['name'],
                             protocol=env['protocol'],
                             ip=env['ip'],
                             port=env['port'],
                             desc=env['desc'],
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status

    # 删除 标记isDeleted
    @staticmethod
    def delete(env_id):
        status = 'ok'
        try:
            data = Environment.objects(id=ObjectId(env_id), isDeleted=False)
            if not data.first():
                return None, 'not_find'
            delete_name = data.first()['name'] + '_已删除_' + env_id
            rs = data.modify(name=delete_name,
                             isDeleted=True,
                             modifiedTime=datetime.utcnow,
                             new=True)
        except InvalidId:
            rs = None
            status = 'not_object_id'
        return convert_mongo_to_json(rs), status
