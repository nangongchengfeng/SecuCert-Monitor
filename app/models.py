# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 16:04
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : models.py.py
# @Software: PyCharm


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ExpirationMonitor(db.Model):
    __tablename__ = 'expiration_monitor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, comment='id')
    service_name = db.Column(db.String(255), nullable=True, comment='关键服务/插件/证书名称')
    use_deploy = db.Column(db.String(255), nullable=True, comment='使用部门')
    deployA = db.Column(db.String(255), nullable=True, comment='管理部门A')
    deployB = db.Column(db.String(255), nullable=True, comment='管理部门B')
    product = db.Column(db.String(255), nullable=True, comment='使用产品')
    scene = db.Column(db.Text, nullable=True, comment='功能场景')
    organ = db.Column(db.String(255), nullable=True, comment='合作方名字')
    manage = db.Column(db.String(255), nullable=True, comment='管理类型')
    manage_id = db.Column(db.String(255), nullable=True, comment='合同编号')
    issuance_date = db.Column(db.DateTime, nullable=True, comment='有效期开始时间')
    expiration_date = db.Column(db.DateTime, nullable=True, comment='有效期结束时间')
    header = db.Column(db.String(255), nullable=True, comment='合同经办人')
    tech = db.Column(db.String(255), nullable=True, comment='技术对接人')
    yumwei = db.Column(db.String(255), nullable=True, comment='巡检人员')
    yumwei_time = db.Column(db.String(255), nullable=True, comment='巡检频率')
    manager = db.Column(db.String(255), nullable=True, comment='关联主管')
    type = db.Column(db.String(255), nullable=False, comment='类型')
    remark = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ExpirationMonitor {self.id} {self.service_name}>'
