import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.notification_service import check_and_notify

scheduler = None


def init_scheduler(app):
    """初始化定时任务调度器"""
    global scheduler

    if scheduler:
        return scheduler

    scheduler = BackgroundScheduler()

    # 从环境变量获取配置，默认每天早上 9 点
    cron_hour = os.getenv('SCHEDULE_HOUR', '9')
    cron_minute = os.getenv('SCHEDULE_MINUTE', '0')

    # 添加定时任务
    scheduler.add_job(
        func=check_and_notify,
        trigger=CronTrigger(hour=int(cron_hour), minute=int(cron_minute)),
        id='certificate_check_job',
        name='证书过期检查任务',
        replace_existing=True
    )

    # 启动调度器
    scheduler.start()

    app.logger.info(f"定时任务已启动，每天 {cron_hour}:{cron_minute} 执行")

    return scheduler


def shutdown_scheduler():
    """关闭调度器"""
    global scheduler
    if scheduler:
        scheduler.shutdown()
        scheduler = None


def get_scheduler():
    """获取调度器实例"""
    return scheduler
