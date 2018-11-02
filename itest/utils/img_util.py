# encoding: utf-8
"""
@author: han.li
@file  : img_util.py
@time  : 8/28/18 4:36 PM
@dec   : 图片相关工具函数集
"""
import xlrd, os
from shutil import copy2
import base64
from PIL import Image, ImageDraw


# 绘制图库
class ImgDeal(object):
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = Image.open(self.img_path)

        self.drew = ImageDraw.Draw(self.img)

    # 根据位置绘制边框
    def drew_frame(self, location):
        x0 = int(location['left'])
        y0 = int(location['top'])
        width = int(location['width'])
        height = int(location['height'])
        node0 = (x0, y0)
        node1 = (x0+width, y0)
        node2 = (x0+width, y0+height)
        node3 = (x0, y0+height)
        self.drew.line((node0, node1, node2, node3, node0), fill=128)

    def drew_number(self, location, number):
        x0 = int(location['left'])
        y0 = int(location['top'])
        width = int(location['width'])
        height = int(location['height'])
        self.drew.text((x0+width-10, y0-10), str(number), 'red')

    def save_img(self, path):
        self.img.save(path)

    def del_drew(self):
        del self.drew

def return_img_stream(img_local_path):
    """
    获取本地图片流
    :param img_local_path: 图片本地绝对路径
    :return: 图片流
    """
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream.decode('ascii')


# 拷贝图片
def copy_image(image_path, path):
    if os.path.isfile(image_path):
        if not os.path.exists(path):
            os.mkdir(path)
        copy2(image_path, path)


#  从execl读取表格信息  取第一列为参数key
def read_excel(fname,tablename,header=0):

    bk = xlrd.open_workbook(fname)
    try:
        table = bk.sheet_by_name(tablename)
    except:
        print("%s没有表格为%s的" % (fname, tablename))
    # 获取行数
    nrows = table.nrows
    # 获取列名
    colnames = table.row_values(header)
    # 获取列数
    ncols = table.ncols
    #print('行数：%s  列数：%s'% (nrows -2, ncols))

    list = []
    for rownum in range(header+1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)

    return list
