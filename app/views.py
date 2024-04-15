# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 16:04
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : views.py.py
# @Software: PyCharm
import time

from flasgger import swag_from
from flask import Blueprint, jsonify, render_template, request
from flask_cors import cross_origin

from app.controller import get_day_less_30_re, get_days_tops, get_datas
from config import dingTalkUrl, dingTalkSecret
from utils.ding_send import sendDingMsg, getDingTalkUrl
from utils.mysql_tools import execute_query

app_views = Blueprint('app_views', __name__)


@app_views.route('/actuator/health', methods=['GET', 'HEAD'])
def health():
    """
    health check
    ---
    tags:
        - 监控
    responses:
        200:
            description: 健康检查
    description: Health check endpoint
    """
    return jsonify({'online': True})


@app_views.route('/', methods=['GET'])
def screen_index():
    """
    大屏显示
    ---
    tags:
        - 监控
    responses:
      200:
        大屏显示
    description: 大屏显示
    """
    data = get_day_less_30_re()
    count = len(data)
    return render_template('screen.html', count=count)


@app_views.route('/index', methods=['GET'])
@cross_origin()
def index():
    """
    数据表格页面
    :return:
    """
    return render_template('table.html')



@app_views.route('/api/data', methods=['GET'])
@cross_origin()
def get_data():
    if request.method == 'GET':
        search_key = request.args.get("search_key")
        # 获取 "page" 参数的值，默认为 1
        page = int(request.args.get("page", 1))

        # 获取 "limit" 参数的值，默认为 10
        limit = int(request.args.get("limit", 10))

        # 打开文件，并以读取模式读取内容
        # with open('output.txt', "r", encoding="utf-8") as file:
        #     content = file.read()
        # # 解析 JSON 数据
        # data_dict = json.loads(content)


        data_lists=get_datas()
        date_list = []
        for i in data_lists:
            # 根据搜索值返回数据
            if search_key:
                if search_key in i["service_name"] or search_key in i["type"] or search_key in i["organ"]:
                    date_list.append(i)
            else:
                date_list.append(i)

        # 打印解析后的JSON数据
        count = len(date_list)
        start = (page - 1) * limit
        end = page * limit
        data = date_list[start:end]
        res = {
            "code": 0,
            "count": count,
            "data": data
        }
        return jsonify(res)


@app_views.route('/get_count_type', methods=['GET'])
def get_count_type():
    """
    获取证书类型的数量
    :return:
    """
    sql = f"""
    SELECT type, COUNT(*) AS count
    FROM expiration_monitor
    GROUP BY type;
    """
    result_list = []
    result = execute_query(sql)
    for item in result:
        result_list.append({'value': item[1], 'name': item[0]})
    return result_list


# 可忽略的证书有效期的数量
@app_views.route('/get_count_day', methods=['GET'])
def get_count_day():
    """

    获取证书有效期的数量
    :return:
    """
    sql = """SELECT validity from cert"""
    data_days = []
    result = execute_query(sql)
    for row in result:
        data_days.append(row[0])
    # 统计小于30的数
    count_less_than_30 = sum(1 for num in data_days if num < 30)
    # 删除小于30的数
    data = [num for num in data_days if num >= 30]

    # 统计小于365的数
    count_less_than_365 = sum(1 for num in data if num < 365)
    # 删除小于365的数
    data = [num for num in data if num >= 365]

    # 统计小于730的数
    count_less_than_730 = sum(1 for num in data if num < 730)
    # 删除小于730的数
    data = [num for num in data if num >= 730]

    # 统计小于1095的数
    count_less_than_1095 = sum(1 for num in data if num < 1095)
    # 删除小于1095的数
    data = [num for num in data if num >= 1095]

    # 统计小于1825的数
    count_less_than_1825 = sum(1 for num in data if num < 1825)
    # 删除小于1825的数
    data = [num for num in data if num >= 1825]

    # 统计小于3650的数
    count_less_than_3650 = sum(1 for num in data if num < 3650)
    # 删除小于3650的数
    data = [num for num in data if num >= 3650]

    # 统计剩余的数
    count_other = len(data)
    count = [count_less_than_30, count_less_than_365, count_less_than_730, count_less_than_1095, count_less_than_1825,
             count_less_than_3650, count_other]

    return count


@app_views.route('/get_count_day_validity', methods=['GET'])
def get_count_day_validity():
    """
    获取证书有效期的数量
    :return:
    """
    sql = """SELECT DATEDIFF(expiration_date, NOW()) AS day_validity   FROM Certificate.expiration_monitor WHERE expiration_date != "NULL"   """
    data_day = []
    result = execute_query(sql)
    for row in result:
        data_day.append(row[0])
    data_days = [num for num in data_day if num >= 0]
    # 统计小于30的数
    count_less_than_30 = sum(1 for num in data_days if num < 30)
    # 删除小于30的数
    data = [num for num in data_days if num >= 30]

    # 统计小于365的数
    count_less_than_365 = sum(1 for num in data if num < 365)
    # 删除小于365的数
    data = [num for num in data if num >= 365]

    # 统计小于730的数
    count_less_than_730 = sum(1 for num in data if num < 730)
    # 删除小于730的数
    data = [num for num in data if num >= 730]

    # 统计小于1095的数
    count_less_than_1095 = sum(1 for num in data if num < 1095)
    # 删除小于1095的数
    data = [num for num in data if num >= 1095]

    # 统计小于1825的数
    count_less_than_1825 = sum(1 for num in data if num < 1825)
    # 删除小于1825的数
    data = [num for num in data if num >= 1825]

    # 统计小于3650的数
    count_less_than_3650 = sum(1 for num in data if num < 3650)
    # 删除小于3650的数
    data = [num for num in data if num >= 3650]

    # 统计剩余的数
    count_other = len(data)
    count = [count_less_than_30, count_less_than_365, count_less_than_730, count_less_than_1095, count_less_than_1825,
             count_less_than_3650, count_other]

    return count


@app_views.route('/get_days_top', methods=['GET'])
def get_days_top():
    """
    根据证书有效期进行排序，获取前10条数据
    :return:
    """

    data_list = get_days_tops()
    count = len(data_list)
    res = {
        "code": 0,
        "count": count,
        "data": data_list
    }
    return res


"""
定时任务的功能实现
需求：获取MySQL数据表中的证书有效期，如果证书有效期小于30天，就发送钉钉给相关人员
"""


@app_views.route('/alerts', methods=['GET'])
def alerts():
    return render_template('alert_table.html')

@app_views.route('/get_day_less_30', methods=['GET'])
def get_day_less_30():
    data = get_day_less_30_re()
    count = len(data)
    res = {
        "code": 0,
        "count": count,
        "data": data
    }
    return res


@app_views.route('/send_alert', methods=['GET'])
def send_alert():
    """
    检查证书即将过期 小于30天,发送钉钉告警
    :return:
    """
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    data = get_day_less_30_re()
    # 过期证书数量
    count = len(data)
    if count == 0:
        print("没有即将过期的证书")
        return "没有即将过期的证书"
    else:
        # 钉钉告警
        service_list = []

        for certificate in data:
            # 提取需要的信息
            # 服务名称
            service_name = certificate['service_name']
            # 过期时间
            expiration_date = certificate['expiration_date']
            # 还有多久过期
            day_validity = certificate['day_validity']
            # 提取负责人、巡检人和相关领导信息
            # 负责人
            header = certificate.get('header', '未提供')
            # 巡检人
            yumwei = certificate.get('yumwei', '未提供')
            # 相关领导
            manager = certificate.get('manager', '未提供')

            # 钉钉告警
            data_dict = {
                "service_name": service_name,
                "expiration_date": expiration_date,
                "days_until_expiry": day_validity,
                "responsible_person": header,
                "inspector": yumwei,
                "manager": manager
            }
            service_list.append(data_dict)
        # 发送钉钉告警
        sendDingMsg(getDingTalkUrl(dingTalkUrl, dingTalkSecret), service_list)
        # sendDingMsg(dingTalkUrl, service_list)
        # print('服务名称：', service_name, '过期时间：', expiration_date, '还有多久过期：', day_validity, '负责人：', header,
        #       '巡检人：', yumwei, '相关领导：', manager)
        return 'success'