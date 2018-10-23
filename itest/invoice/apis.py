# encoding: utf-8
"""
@author: han.li
@file  : apis.py
@time  : 8/28/18 10:00 AM
@dec   : 
"""


from flask import Blueprint, request
import json
from bson import ObjectId
from .models import Invoice
from itest.utils.img_util import return_img_stream
from itest.utils.utils import init_return
from .invoke import verify_invoke
"""
    发票识别查验相关接口
    图片相关：
    1 根据图片id获取图片数据接口
    2 获取所有图片信息接口
    3 修改图片五要素接口
    
    发票识别：
    1 根据图片id或图片路径调用识别接口
    2 显示发票识别结果
    
    发票查验：
    1 根据发票五要素调用发票查验接口
    2 显示发票查验结果
"""
blueprint = Blueprint('invoice', __name__)


@blueprint.route('/images/<image_id>', methods=['GET', 'POST'])
def get_image(image_id):
    """
     1 根据图片id获取图片数据接口
    :param: image_id
    :return:
    """
    inv = Invoice.objects(id=ObjectId(image_id)).first()
    data = inv.to_dict()
    image_path = data['image_path']
    return init_return(return_img_stream(image_path))


@blueprint.route('/images/delete/<image_id>', methods=['GET', 'POST'])
def delete_images(image_id):
    """
     1 根据图片id删除图片数据接口
    :param: image_id
    :return:
    """
    print(image_id)
    result = Invoice.objects(id=ObjectId(image_id)).delete()
    return init_return(result)


@blueprint.route('/images', methods=['GET', 'POST'])
def get_images():
    """
     2 获取所有图片信息接口
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    page = data['page']
    image_from = data['image_from']
    checked = data['checked']
    page_size = data['page_size']
    if 'image_name' in data and data['image_name']!='':
        image_name = data['image_name']
        # invoices = Invoice.objects(image_name=image_name)[page_size * (page - 1):page_size * page]
        # total = Invoice.objects(image_name=image_name).count()
        page = int(image_name) + page + 5
        invoices = Invoice.objects(image_from=image_from, checked=checked)[page_size * (page - 1):page_size * page]
        total = Invoice.objects(image_from=image_from, checked=checked).count()
    else:
        invoices = Invoice.objects(image_from=image_from, checked=checked)[page_size*(page-1):page_size*page]
        total = Invoice.objects(image_from=image_from, checked=checked).count()
    data = []
    for invoice in invoices:
        data.append(invoice.to_dict())
    info ={
            "total": total,
            "data": data
        }
    return init_return(info)


@blueprint.route('/images/update', methods=['GET', 'POST'])
def update_image():
    """
      3 修改图片五要素接口
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    id = data['id']

    invoice = Invoice.objects(id=ObjectId(id))
    if invoice.count() == 0:
        return init_return({}, sucess=False, error="更新失败（id: %s 找不到数据）" % id, errorCode=1001)
    else:
        if 'checked' in data:
            invoice.update_one(checked=data['checked'])
        if 'detail' in data:
            invoice.update_one(detail=data['detail'])
        if 'image_from' in data:
            invoice.update_one(image_from=data['image_from'])
        return init_return({})


@blueprint.route('/recognize', methods=['GET', 'POST'])
def recognize():
    """
      1 发票识别接口
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    image_path = data['image_path']
    print(image_path)
    return init_return(image_path)


@blueprint.route('/verify', methods=['GET', 'POST'])
def verify():
    """
      2 发票查验接口
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    detail = data['detail']
    return verify_invoke(detail)


@blueprint.route('/task', methods=['GET', 'POST'])
def get_task():
    """
      2 发票识别任务
    :return:
    """
    data = json.loads(request.get_data().decode('utf-8'))
    name = data['task_name']
    page = data['page']
    page_size = data['page_size']
    # task = Task.objects(name=name).first()
    # query_task = []
    # if 'expect_status' in data and data['expect_status'] !=[]:
    #     expect_status = data['expect_status']
    #     for t in task['result']:
    #         if t['expect']['status'] in expect_status:
    #             query_task.append(t)
    #
    #     result = {
    #         'total': len(query_task),
    #         'summary': task['summary'],
    #         'data': query_task[page_size * (page - 1):page_size * (page)]
    #     }
    # else:
    #     result = {
    #         'total': len(task['result']),
    #         'summary': task['summary'],
    #         'data': task['result'][page_size*(page-1):page_size*(page)]
    #     }

    # return init_return(result)
