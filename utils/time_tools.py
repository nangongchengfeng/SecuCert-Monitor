# -*- coding: utf-8 -*-
# @Time    : 2023/9/27 10:16
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : time_tools.py
# @Software: PyCharm
from datetime import datetime, date


# 计算两个日期之间的日期差
def calculate_date_difference(start_date, end_date):
    print(start_date, end_date)
    # 计算日期差距
    delta = end_date - start_date

    # 提取天数差距
    days_difference = delta.days

    return days_difference


# 定义一个函数，用于获取格式化的日期
def get_formatted_date():
    # 获取当前时间
    today = date.today()

    # 返回格式化的日期
    return today
if __name__ == '__main__':
    print(type(get_formatted_date()))
