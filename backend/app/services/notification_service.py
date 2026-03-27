import base64
import hashlib
import hmac
import json
import time
import urllib
import os
from datetime import datetime, timedelta
import requests
from app.extensions import db
from app.models import ExpirationMonitor, NotificationLog


def get_dingtalk_url(webhook_url, secret):
    """生成带签名的钉钉 webhook URL"""
    if not secret:
        return webhook_url

    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return webhook_url + "&timestamp=" + timestamp + "&sign=" + sign


def is_notified_today(cert_id):
    """检查今天是否已经通知过"""
    today = datetime.now().date()
    return NotificationLog.query.filter(
        NotificationLog.certificate_id == cert_id,
        db.func.date(NotificationLog.notification_date) == today
    ).first() is not None


def get_expiring_certificates(days=30):
    """获取即将过期的证书"""
    today = datetime.now().date()
    target_date = today + timedelta(days=days)

    certificates = ExpirationMonitor.query.filter(
        ExpirationMonitor.expiration_date >= today,
        ExpirationMonitor.expiration_date <= target_date
    ).order_by(ExpirationMonitor.expiration_date.asc()).all()

    return certificates


def build_notification_message(certificates):
    """构建钉钉通知消息（Markdown格式）"""
    title = "证书过期提醒"
    keywords = os.getenv('DINGTALK_KEYWORDS', '证书,过期,告警').split(',')
    keyword_list = []
    for k in keywords:
        k_stripped = k.strip()
        if k_stripped:
            keyword_list.append(k_stripped)
    keyword_text = ' '.join(keyword_list)

    text = '''<font color='#FF0000'><b>[证书巡检]</b></font> <b>''' + title + ''' ''' + keyword_text + '''</b>

---

'''

    for cert in certificates:
        if cert.expiration_date:
            today = datetime.now().date()
            exp_date = cert.expiration_date.date()
            days_remaining = (exp_date - today).days
        else:
            days_remaining = '未知'

        text += '''<font color='#778899' size=2><b>证书名称：</b> ''' + (cert.service_name or '-') + '''</font>

'''
        text += '''<font color='#708090' size=2><b>过期日期：</b> ''' + (cert.expiration_date.strftime('%Y-%m-%d') if cert.expiration_date else '-') + '''</font>

'''
        text += '''<font color='#708090' size=2><b>剩余天数：</b> ''' + str(days_remaining) + ''' 天</font>

'''
        text += '''<font color='#708090' size=2><b>类型：</b> ''' + (cert.type or '-') + '''</font>

'''
        text += '''<font color='#708090' size=2><b>负责人：</b> ''' + (cert.header or '-') + '''</font>

'''
        text += '''<font color='#708090' size=2><b>使用部门：</b> ''' + (cert.use_deploy or '-') + '''</font>

---

'''

    text += '''<font color='#708090' size=2><b>备注：</b> 请及时处理并更新证书信息</font>

'''

    return {
        "msgtype": "markdown",
        "markdown": {
            "title": "证书过期提醒",
            "text": text
        }
    }


def send_dingtalk_message(webhook_url, secret, certificates):
    """发送钉钉消息"""
    if not webhook_url:
        return False, "未配置钉钉 Webhook"

    try:
        url = get_dingtalk_url(webhook_url, secret)
        data = build_notification_message(certificates)
        headers = {"Content-Type": "application/json"}

        print(f"发送钉钉消息到: {url[:80]}...")
        print(f"消息内容: {json.dumps(data, ensure_ascii=False)[:200]}...")

        res = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
        result = res.json()

        print(f"钉钉响应: {json.dumps(result, ensure_ascii=False)}")

        if result.get('errcode') == 0:
            return True, None
        else:
            return False, result.get('errmsg', '未知错误')

    except Exception as e:
        print(f"发送异常: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)


def log_notification(cert, days_remaining, success, error_msg=None):
    """记录通知日志"""
    log = NotificationLog(
        certificate_id=cert.id,
        days_remaining=days_remaining,
        sent_success=success,
        error_message=error_msg,
        notification_type='dingtalk'
    )
    db.session.add(log)
    db.session.commit()


def check_and_notify():
    """检查证书并发送通知（主函数）"""
    webhook_url = os.getenv('DINGTALK_WEBHOOK')
    secret = os.getenv('DINGTALK_SECRET')
    notify_days = int(os.getenv('NOTIFY_DAYS_BEFORE', '30'))

    if not webhook_url:
        print("未配置钉钉 Webhook，跳过通知")
        return

    certificates = get_expiring_certificates(days=notify_days)

    if not certificates:
        print("没有即将过期的证书")
        return

    to_notify = []
    for cert in certificates:
        if not is_notified_today(cert.id):
            to_notify.append(cert)

    if not to_notify:
        print("今天已经全部通知过了")
        return

    print("准备通知 " + str(len(to_notify)) + " 个证书")

    success, error_msg = send_dingtalk_message(webhook_url, secret, to_notify)

    for cert in to_notify:
        if cert.expiration_date:
            today = datetime.now().date()
            exp_date = cert.expiration_date.date()
            days_remaining = (exp_date - today).days
        else:
            days_remaining = -1

        log_notification(cert, days_remaining, success, error_msg if not success else None)

    if success:
        print("钉钉通知发送成功")
    else:
        print("钉钉通知发送失败: " + (error_msg or ''))
