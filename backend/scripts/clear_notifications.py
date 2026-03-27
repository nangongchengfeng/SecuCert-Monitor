import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import NotificationLog


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        count = NotificationLog.query.count()
        print(f"准备删除 {count} 条通知日志...")
        NotificationLog.query.delete()
        db.session.commit()
        print("删除完成！")
