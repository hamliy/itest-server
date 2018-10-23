# encoding: utf-8
"""
@author: han.li
@file  : img_util.py
@time  : 8/28/18 4:36 PM
@dec   : 图片相关工具函数集
"""
import xlrd

def return_img_stream(img_local_path):
    """
    获取本地图片流
    :param img_local_path: 图片本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

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
