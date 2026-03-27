from app.extensions import db
from datetime import datetime


class NotificationLog(db.Model):
    __tablename__ = 'notification_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    certificate_id = db.Column(db.Integer, db.ForeignKey('expiration_monitor.id'), nullable=False, comment='证书ID')
    notification_date = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='通知日期')
    notification_type = db.Column(db.String(50), nullable=False, default='dingtalk', comment='通知类型')
    days_remaining = db.Column(db.Integer, nullable=False, comment='剩余天数')
    sent_success = db.Column(db.Boolean, nullable=False, default=True, comment='是否发送成功')
    error_message = db.Column(db.Text, nullable=True, comment='错误信息')

    certificate = db.relationship('ExpirationMonitor', backref=db.backref('notifications', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'certificate_id': self.certificate_id,
            'notification_date': self.notification_date.isoformat() if self.notification_date else None,
            'notification_type': self.notification_type,
            'days_remaining': self.days_remaining,
            'sent_success': self.sent_success,
            'error_message': self.error_message
        }

    def __repr__(self):
        return f'<NotificationLog {self.id} cert={self.certificate_id}>'
