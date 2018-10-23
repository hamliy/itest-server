# encoding: utf-8
"""
@author: han.li
@file  : interface_apis.py
@time  : 9/6/18 2:24 PM
@dec   : 
"""

"""
    接口基本功能api：
    1、查看全部
    2、根据id查看
    3、新增
    4、修改
    5、删除
"""

from flask import Blueprint, request
from itest.models import Interface, Project, Theme
from bson import ObjectId
from itest.utils.utils import init_return, mongo_to_dict, get_value, convert_mongo_to_json
from itest.utils.decorators import params_required, params_objectid_check, project_check, params_empty_check

blueprint = Blueprint('interface', __name__)



@blueprint.route('/all', methods=['GET', 'POST'])
@params_objectid_check(['project_id'])
@params_required(['project_id'])
def all_interfaces():
    """
     1 获取所有接口信息接口,根据项目
    :return:
    """
    data = request.get_json()
    # data = json.loads(request.get_data().decode('utf-8'))
    page = 1
    page_size = 20
    project_id = data['project_id']

    if 'page' in data and 'page_size' in data:
        page = data['page']
        page_size = data['page_size']

    interfaces = Interface.objects(project=ObjectId(project_id))[page_size * (page - 1):page_size * page]
    total = Interface.objects(project=ObjectId(project_id)).count()
    data = []
    for interface in interfaces:
        data.append(convert_mongo_to_json(interface))
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)


@blueprint.route('/<interface_id>', methods=['GET', 'POST'])
def get_interface(interface_id):
    """
     2、根据id查看
    :param: environment_id
    :return:
    """
    interface = Interface.objects(id=ObjectId(interface_id))
    if interface.count() == 0:
        return init_return({}, sucess=False, error="查找的接口不存在", errorCode=1001)
    else:
        return init_return(convert_mongo_to_json(interface.first()))


@blueprint.route('/create', methods=['GET', 'POST'])
@project_check
@params_required(['project_id', 'name', 'interface', 'type'])
def add():
    """
      3 新增接口
    :return:
    """
    data = request.get_json()
    # data = json.loads(request.get_data().decode('utf-8'))

    project_id = data['project_id']
    name = data['name']
    interface = data['interface']
    request_type = data['type']

    if request_type not in ['post', 'get']:
        return init_return({}, sucess=False, error="type不能为%s" % request_type, errorCode=1001)

    content_type = get_value(data, 'content_type')
    params = get_value(data, 'params', [])
    headers = get_value(data, 'headers', [])
    description = get_value(data, 'description')

    existed = Interface.objects(name=name, project=ObjectId(project_id)).first()
    if existed:
        return init_return({}, sucess=False, error="存在相同接口名", errorCode=1001)

    Interface(name=name, project=ObjectId(project_id), interface=interface, headers=headers,
              request_type=request_type, content_type=content_type, params=params, remarks={'description':description}).save()
    return init_return({
        'data': '新增成功'
    })


@blueprint.route('/update', methods=['GET', 'POST'])
@params_empty_check(['name', 'interface', 'type'])
@params_required(['id'])
def update():
    """
      4 根据接口id更新接口
    :return:
    """
    data = request.get_json()
    # data = json.loads(request.get_data().decode('utf-8'))
    id = data['id']
    name = data['name']
    interf = data['interface']
    request_type = data['type']

    interface = Interface.objects(id=ObjectId(id))
    if interface.count() == 0:
        return init_return({}, sucess=False, error="更新的接口不存在", errorCode=1001)
    else:
        existed = Interface.objects(name=name, project=interface.first().project).first()
        if existed and str(existed.id) != id:
            return init_return({}, sucess=False, error="存在相同环境名", errorCode=1001)

        content_type = get_value(data, 'content_type')
        params = get_value(data, 'params', [])
        headers = get_value(data, 'headers', [])
        description = get_value(data, 'description')

        source = mongo_to_dict(interface.first())

        if name != source['name']:
            interface.update_one(name=name)
        if interf != source['interface']:
            interface.update_one(interface=interf)
        if params != source['params']:
            interface.update_one(params=params)
        if content_type != source['content_type']:
            interface.update_one(content_type=content_type)
        if request_type != source['request_type']:
            interface.update_one(request_type=request_type)
        if headers != source['headers']:
            interface.update_one(headers=headers)
        if description != source['remarks']['description']:
            interface.update_one(remarks__description=description)

        return init_return({
            'data': '更新成功'
        })


@blueprint.route('/delete/<interface_id>', methods=['GET', 'POST'])
def delete(interface_id):
    """
     5 根据项目id删除项目接口
    :param: interface_id
    :return:
    """
    if not ObjectId.is_valid(interface_id):
        return init_return({}, sucess=False, error="接口id参数错误", errorCode=1001)

    result = Interface.objects(id=ObjectId(interface_id)).delete()
    if result == 0:
        return init_return({}, sucess=False, error="删除的接口不存在", errorCode=1001)
    else:
        return init_return({'data': '删除成功'})


@blueprint.route('/theme/create', methods=['POST'])
@project_check
@params_required(['project_id', 'name'])
def theme_add():
    """
      6 新增主题或接口
    :return:
    """
    data = request.get_json()
    # data = json.loads(request.get_data().decode('utf-8'))

    project_id = data['project_id']
    name = data['name']

    desc = get_value(data, 'desc', '')
    existed = Theme.objects(name=name, project_id=ObjectId(project_id)).first()
    if existed:
        return init_return({}, sucess=False, error="存在相同主题名", errorCode=1001)

    Theme(name=name, project_id=ObjectId(project_id), desc=desc, list=[], sub_themes=[]).save()

    return init_return({
        'data': '新增成功'
    })

@blueprint.route('/theme/create/sub', methods=['POST'])
@project_check
@params_required(['theme_id', 'name'])
def theme_add_sub():
    """
      6 新增主题对应接口
    :return:
    """
    data = request.get_json()
    # data = json.loads(request.get_data().decode('utf-8'))

    name = data['name']
    theme_id = data['theme_id']
    desc = get_value(data, 'desc', '')

    # 新增子主题
    node = convert_mongo_to_json(Theme.objects(id=ObjectId(theme_id)).first())

    if len(node['sub_themes']) != 0 and \
            len(list(filter(lambda x: x['name'] == name, node['sub_themes']))) != 0:
        return init_return({}, sucess=False, error="存在相同子主题名", errorCode=1001)
    subtheme = {
        'desc': desc,
        'name': name,
        'list': []
    }
    Theme.objects(id=ObjectId(theme_id)).update_one(push__sub_themes=subtheme)

    return init_return({
        'data': '新增成功'
    })

@blueprint.route('/theme/create/interface', methods=['POST'])
@project_check
@params_required(['theme_id', 'name'])
def theme_add_interface():
    """
      6 新增主题对应接口
    :return:
    """
    data = request.get_json()

    theme_id = data['theme_id']
    name = data['name']
    desc = get_value(data, 'desc', '')
    sub_theme_name = get_value(data, 'sub_theme_name', '')

    # 新增接口
    node = convert_mongo_to_json(Theme.objects(id=ObjectId(theme_id)).first())
    interface = {
        'desc': desc,
        'name': name
    }
    int
    # 主节点
    if sub_theme_name == '':

        if len(node['list']) != 0 and \
                len(list(filter(lambda x:  x['name'] == name, node['list']))) != 0:
            return init_return({}, sucess=False, error="存在相同接口名", errorCode=1001)
        Theme.objects(id=ObjectId(theme_id)).update_one(push__list=interface)

    else:
        node = list(filter(lambda x: x['name'] == sub_theme_name, node['sub_themes']))[0]\
                or {'list': []}

        if len(node['list']) != 0 and \
                len(list(filter(lambda x: x['name'] == name, node['list']))) != 0:
            return init_return({}, sucess=False, error="该主题下存在相同接口名", errorCode=1001)

        theme = Theme.objects(id=ObjectId(theme_id), sub_themes__name=sub_theme_name)
        theme.update_one(push__sub_themes__S__list=interface)

    return init_return({
        'data': '新增成功'
    })

@blueprint.route('/theme/remove', methods=['GET', 'POST'])
@params_required(['theme_id'])
def theme_remove():
    """
     5 接口删除
    :param: interface_id
    :return:
    """
    data = request.get_json()
    theme_id = data['theme_id']
    if not ObjectId.is_valid(theme_id):
        return init_return({}, sucess=False, error="theme_id参数错误", errorCode=1001)

    # 删除主节点
    result = Theme.objects(id=ObjectId(theme_id)).delete()
    if result == 0:
        return init_return({}, sucess=False, error="删除的主题不存在", errorCode=1001)
    else:
        return init_return({'data': '删除成功'})


@blueprint.route('/theme/remove/sub', methods=['GET', 'POST'])
@params_required(['theme_id', 'sub_theme_name'])
def theme_remove_sub():
    """
     5 接口删除
    :param: interface_id
    :return:
    """
    data = request.get_json()
    sub_theme_name = data['sub_theme_name']
    theme_id = data['theme_id']
    if not ObjectId.is_valid(theme_id):
        return init_return({}, sucess=False, error="theme_id参数错误", errorCode=1001)

    # 删除子主题
    result = Theme.objects(id=ObjectId(theme_id)).update_one(pull__sub_themes__name=sub_theme_name)
    if result == 0:
        return init_return({}, sucess=False, error="删除的子主题不存在", errorCode=1001)
    else:
        return init_return({'data': '删除成功'})


@blueprint.route('/theme/remove/interface', methods=['GET', 'POST'])
@params_required(['theme_id', 'sub_theme_name', 'interface_id'])
def theme_remove_infterface():
    """
     5 接口删除
    :param: interface_id
    :return:
    """
    data = request.get_json()
    sub_theme_name = data['sub_theme_name']
    interface_id = data['interface_id']
    theme_id = data['theme_id']
    if not ObjectId.is_valid(theme_id):
        return init_return({}, sucess=False, error="theme_id参数错误", errorCode=1001)

    # 主节点
    if sub_theme_name == '':
        result = Theme.objects(id=ObjectId(theme_id)).update_one(pull__list__interface_id=ObjectId(interface_id))
        if result == 0:
            return init_return({}, sucess=False, error="删除的接口不存在", errorCode=1001)
        else:
            return init_return({'data': '删除成功'})
    else:
        theme = Theme.objects(id=ObjectId(theme_id), sub_themes__name=sub_theme_name)
        result = theme.update_one(pull__sub_themes__S__list__interface_id=ObjectId(interface_id))
        if result == 0:
            return init_return({}, sucess=False, error="删除的接口不存在", errorCode=1001)
        else:
            return init_return({'data': '删除成功'})


@blueprint.route('/theme/all', methods=['GET', 'POST'])
@params_objectid_check(['project_id'])
@params_required(['project_id'])
def all_themes():
    """
     7 获取所有接口主题信息接口,根据项目
    :return:
    """
    data = request.get_json()

    project_id = data['project_id']

    themes = Theme.objects(project_id=ObjectId(project_id))
    total = Theme.objects(project_id=ObjectId(project_id)).count()
    data = []
    for theme in themes:
        data.append(convert_mongo_to_json(theme))
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)
