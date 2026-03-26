import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db


def init_db():
    app = create_app()

    with app.app_context():
        db.create_all()
        print("数据库表创建成功！")


if __name__ == '__main__':
    init_db()
