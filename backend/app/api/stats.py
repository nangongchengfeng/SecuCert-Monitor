from flask import Blueprint
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.extensions import db
from app.models import ExpirationMonitor
from app.api.schemas import APIResponse

stats_bp = Blueprint('stats', __name__, url_prefix='/api')


@stats_bp.route('/stats/overview', methods=['GET'])
def get_overview():
    today = datetime.now().date()
    thirty_days = today + timedelta(days=30)
    ninety_days = today + timedelta(days=90)

    total = ExpirationMonitor.query.count()

    expired = ExpirationMonitor.query.filter(
        ExpirationMonitor.expiration_date < today).count()

    urgent = ExpirationMonitor.query.filter(
        and_(
            ExpirationMonitor.expiration_date >= today,
            ExpirationMonitor.expiration_date <= thirty_days
        )
    ).count()

    warning = ExpirationMonitor.query.filter(
        and_(
            ExpirationMonitor.expiration_date > thirty_days,
            ExpirationMonitor.expiration_date <= ninety_days
        )
    ).count()

    normal = ExpirationMonitor.query.filter(
        ExpirationMonitor.expiration_date > ninety_days
    ).count()

    return APIResponse(
        code=0,
        message="success",
        data={
            'total': total,
            'expired': expired,
            'urgent': urgent,
            'warning': warning,
            'normal': normal
        }
    ).model_dump()


@stats_bp.route('/stats/by-type', methods=['GET'])
def get_by_type():
    results = db.session.query(
        ExpirationMonitor.type, func.count(ExpirationMonitor.id)
    ).group_by(ExpirationMonitor.type).all()

    data = [{'type': r[0], 'count': r[1]} for r in results]

    return APIResponse(code=0, message="success", data=data).model_dump()


@stats_bp.route('/stats/expiring', methods=['GET'])
def get_expiring():
    today = datetime.now().date()
    thirty_days = today + timedelta(days=30)

    certificates = ExpirationMonitor.query.filter(
        and_(
            ExpirationMonitor.expiration_date >= today,
            ExpirationMonitor.expiration_date <= thirty_days
        )
    ).order_by(ExpirationMonitor.expiration_date.asc()).limit(10).all()

    data = []
    for cert in certificates:
        cert_dict = cert.to_dict()
        if cert.expiration_date:
            exp_date = cert.expiration_date.date()
            cert_dict['day_validity'] = (exp_date - today).days
        data.append(cert_dict)

    return APIResponse(code=0, message="success", data=data).model_dump()
