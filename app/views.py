# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 16:04
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : views.py.py
# @Software: PyCharm
from flask import Blueprint

app_views = Blueprint('app_views', __name__)





@app_views.route('/')
def home():
    return 'Welcome! You are logged in.'