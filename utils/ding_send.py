# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 17:08
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ding_send.py
# @Software: PyCharm
import base64
import hashlib
import hmac
import json
import time
import urllib

import requests


def getDingTalkUrl(url, secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return url + "&timestamp=" + timestamp + "&sign=" + sign;


def sendDingMsg(url, msg):
    # 请求头
    headers = {"Content-Type": "application/json"}

    title = "证书过期提醒"

    # 构建大屏地址
    big_url = 'http://172.31.161.175:5000'
    # 初始胡文本
    text = f'''<font color=\'#FF0000\'><b>[巡检]</b> </font><b>{title}</b>\n\n --- \n\n'''

    # 处理巡检信息
    for item in msg:
        text += f'''<font color=\'#778899\' size=2><b>巡检标题：</b> {item['service_name']}</font>\n\n '''
        text += f'''<font color=\'#708090\' size=2><b>巡检内容：</b>\n\n到期时间：{item['expiration_date']}\n\n距离失效（天）：{item['days_until_expiry']}\n\n 负责人：{item['responsible_person']}\n\n 巡检人：{item['inspector']}\n\n 巡检人：{item['manager']}</font>\n\n\n\n <br> '''
    text += f'''<font color=\'#708090\' size=2><b>详情：</b> [点击查看详情](%s)</font>\n\n ''' % big_url
    text += f'''<font color=\'#778899\' size=2><b>备注：</b> 请及时处理并联系-系统运维更改: 到期时间</font>\n\n '''
    # 构建钉钉消息数据
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "巡检提醒",
            "text": text
        }
    }
    # 发送钉钉消息
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print("#Send DingTalk robot res:" + str(res.text))
