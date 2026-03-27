import sys
import os
import json
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv('DINGTALK_WEBHOOK')
secret = os.getenv('DINGTALK_SECRET')

print("=== 钉钉机器人测试 ===\n")
print(f"Webhook: {webhook_url[:60]}..." if webhook_url else "Webhook: 未配置")
print(f"Secret: {'已配置' if secret else '未配置'}\n")

if not webhook_url:
    print("错误：请先配置 DINGTALK_WEBHOOK")
    sys.exit(1)

# 构建最简单的测试消息
test_data = {
    "msgtype": "text",
    "text": {
        "content": "证书 过期 告警 - 这是一条测试消息"
    }
}

print("发送测试消息...")
print(f"URL: {webhook_url[:80]}...")
print(f"Data: {json.dumps(test_data, ensure_ascii=False)}\n")

try:
    # 先测试不加签的方式
    res = requests.post(webhook_url, data=json.dumps(test_data),
                       headers={"Content-Type": "application/json"},
                       timeout=10)

    result = res.json()
    print(f"响应状态码: {res.status_code}")
    print(f"响应内容: {json.dumps(result, ensure_ascii=False)}")

    if result.get('errcode') == 0:
        print("\n✅ 测试消息发送成功！")
    else:
        print(f"\n❌ 发送失败: {result.get('errmsg')}")
        print("\n提示：请检查钉钉机器人安全设置，确保已添加关键词 '证书'、'过期' 或 '告警'")

except Exception as e:
    print(f"\n❌ 请求异常: {e}")
    import traceback
    traceback.print_exc()
