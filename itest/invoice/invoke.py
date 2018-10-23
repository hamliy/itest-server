# encoding: utf-8
"""
@author: han.li
@file  : invoke.py
@time  : 8/29/18 2:39 PM
@dec   : 
"""
"""
    发票相关调用方法
"""
import requests
from itest.utils.utils import init_return


# 发票类型，01：纸质专用发票；03：机动车发票；04：纸质普通发票；10：电子发票；11：普通卷票
def judge_type(invoice_code):
    c = '99'
    default_code = ["144031539110", "131001570151", "133011501118", "111001571071"]

    if len(invoice_code) == 12:
        # default 10
        if invoice_code in default_code:
            c = '10'

        if c == '99':
            # 增加判断，判断是否为新版电子票 第1位为0且第11-12位为11
            if invoice_code[0] == '0' and invoice_code[10:12] == '11':
                c = '10'
            # 判断是否为卷式发票 第1位为0且第11-12位为06或07
            if invoice_code[0] == '0' and (invoice_code[10:12] == '06' or invoice_code[10:12] == '07'):
                c = '11'
        # 如果还是99，且第8位是2，则是机动车发票
        if c == '99':
            b = invoice_code[7]
            if b == '2' and invoice_code[0] != '0':
                c = '03'
    elif len(invoice_code) == 10:
        b = invoice_code[7]
        if b in ['1', '5']:
            c = '01'
        elif b in ['6', '3']:
            c = '04'
        elif b in ['7', '2']:
            c = '02'
    return c


def verify_invoke(five):
    url = 'http://120.92.208.58:31164/brp/invoice/verification'
    type = judge_type(five['fpdm'])
    if type not in ['01', '03']:
        fpje = five['jym']
    else:
        fpje = five['fpje']
    data = {
        'fpdm': five['fpdm'],
        'fphm': five['fphm'],
        'kprq': five['kprq'],
        'fpje': fpje,
        'accessKeyId': 'research$2017'
    }
    resp = requests.post(url, headers={}, data=data, timeout=float(60000))
    # if resp == 'error':
    #     return 'error'
    # 请求异常不是200
    if resp is None or resp.status_code != 200:
        status = 0
        if resp is None:
            error = "response was None !"
            data = resp
        else:
            error = "status_code == %s not 200" % resp.status_code
            data = resp.text
        return init_return(data=data, sucess=False, errorCode=1001, error=error)
    data = resp.text
    print(data)
    return init_return(data=data)