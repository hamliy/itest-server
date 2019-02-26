# encoding: utf-8
"""
@author: han.li
@file  : s_test_reports.py
@time  : 1/15/19 4:59 PM
@dec   : 测试报告操作
"""
from itest.model.m_test_reports import TestReports
import datetime
import os
from bson import ObjectId
from itest.utils import separator
from itest.utils.request import get_user_id


def add_test_reports(runner, report_name=None):
    """
    定时任务或者异步执行报告信息落地
    :param start_at: time: 开始时间
    :param report_name: str: 报告名称，为空默认时间戳命名
    :param kwargs: dict: 报告结果值
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    runner.summary['time']['start_datetime'] = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    report_name = report_name if report_name else runner.summary['time']['start_datetime']
    runner.summary['html_report_name'] = report_name

    report_path = os.path.join(os.getcwd(), "reports{}{}.html".format(separator, int(runner.summary['time']['start_at'])))
    runner.gen_html_report(html_report_template=os.path.join(os.getcwd(), "templates{}extent_report_template.html".format(separator)))

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()
    creator_id = get_user_id()
    test_reports = {
        'name': report_name,
        'belongProjectId': '',
        'creatorId': ObjectId(creator_id),
        'status': runner.summary.get('success'),
        'stat': runner.summary.get('stat'),
        'startTime': runner.summary['time']['start_datetime'],
        'reports': reports
    }

    TestReports(test_reports).save()
    return report_path
