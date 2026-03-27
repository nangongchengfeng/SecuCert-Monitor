import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.notification_service import check_and_notify


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        print("手动触发证书检查和钉钉通知...")
        check_and_notify()
        print("完成")
