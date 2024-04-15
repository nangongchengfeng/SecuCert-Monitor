# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 16:02
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : __init__.py
# @Software: PyCharm
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask

from app.views import app_views, send_alert
from flasgger import Swagger, swag_from

from exts import db


def create_app():
    app = Flask(__name__,template_folder='../templates',static_folder='../static')
    Swagger(app)
    app.config.from_object('config.Config')
    # 数据库初始化
    # db.init_app(app)

    app.register_blueprint(app_views)
    # 创建一个后台调度器
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    # 添加一个每隔20秒执行一次的定时任务
    # scheduler.add_job(func=send_alert, trigger="interval", seconds=20)
    # 添加一个每天早上9点执行的定时任务
    scheduler.add_job(func=send_alert, trigger=CronTrigger(hour=9, minute=0))
    # 启动调度器
    scheduler.start()

    return app
