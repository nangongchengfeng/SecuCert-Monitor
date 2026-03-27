from flask import Flask
from app.config import Config
from app.extensions import db, cors
from app.api import certificates_bp, stats_bp, health_bp
from app.tasks.scheduler import init_scheduler, shutdown_scheduler
import atexit


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": ["http://localhost:5173"]}})

    app.register_blueprint(certificates_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(health_bp)

    # 初始化定时任务
    init_scheduler(app)

    # 应用退出时关闭调度器
    atexit.register(shutdown_scheduler)

    @app.errorhandler(404)
    def not_found(error):
        return {"code": 404, "message": "资源不存在", "data": None}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"code": 500, "message": "服务器内部错误", "data": None}, 500

    return app
