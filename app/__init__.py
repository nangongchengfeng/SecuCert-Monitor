# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 16:02
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : __init__.py
# @Software: PyCharm
from flask import Flask

from app.views import app_views


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.register_blueprint(app_views)

    return app