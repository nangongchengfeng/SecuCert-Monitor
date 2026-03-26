from flask import Blueprint, request
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.extensions import db
from app.models import ExpirationMonitor
from app.api.schemas import APIResponse, CertificateCreate, CertificateUpdate

certificates_bp = Blueprint('certificates', __name__, url_prefix='/api')


def get_day_validity(cert):
    if not cert.expiration_date:
        return None
    today = datetime.now().date()
    exp_date = cert.expiration_date.date()
    return (exp_date - today).days


@certificates_bp.route('/certificates', methods=['GET'])
def get_certificates():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    query = ExpirationMonitor.query

    if search:
        query = query.filter(
            ExpirationMonitor.service_name.contains(search))

    if status_filter:
        today = datetime.now().date()
        if status_filter == 'expired':
            query = query.filter(ExpirationMonitor.expiration_date < today)
        elif status_filter == 'urgent':
            thirty_days = today + timedelta(days=30)
            query = query.filter(
                and_(
                    ExpirationMonitor.expiration_date >= today,
                    ExpirationMonitor.expiration_date <= thirty_days
                )
            )
        elif status_filter == 'normal':
            thirty_days = today + timedelta(days=30)
            query = query.filter(ExpirationMonitor.expiration_date > thirty_days)

    pagination = query.order_by(ExpirationMonitor.expiration_date.asc()).paginate(
        page=page, per_page=per_page, error_out=False)

    certificates = pagination.items
    data = []
    for cert in certificates:
        cert_dict = cert.to_dict()
        cert_dict['day_validity'] = get_day_validity(cert)
        data.append(cert_dict)

    return APIResponse(
        code=0,
        message="success",
        data={
            'items': data,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }
    ).model_dump()


@certificates_bp.route('/certificates/<int:cert_id>', methods=['GET'])
def get_certificate(cert_id):
    cert = ExpirationMonitor.query.get_or_404(cert_id)
    cert_dict = cert.to_dict()
    cert_dict['day_validity'] = get_day_validity(cert)
    return APIResponse(code=0, message="success", data=cert_dict).model_dump()


@certificates_bp.route('/certificates', methods=['POST'])
def create_certificate():
    data = request.get_json()
    cert_data = CertificateCreate(**data)

    cert = ExpirationMonitor(**cert_data.model_dump())
    db.session.add(cert)
    db.session.commit()

    return APIResponse(code=0, message="创建成功", data=cert.to_dict()).model_dump()


@certificates_bp.route('/certificates/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):
    cert = ExpirationMonitor.query.get_or_404(cert_id)
    data = request.get_json()
    cert_data = CertificateUpdate(**data)

    for key, value in cert_data.model_dump(exclude_unset=True).items():
        setattr(cert, key, value)

    db.session.commit()

    return APIResponse(code=0, message="更新成功", data=cert.to_dict()).model_dump()


@certificates_bp.route('/certificates/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    cert = ExpirationMonitor.query.get_or_404(cert_id)
    db.session.delete(cert)
    db.session.commit()

    return APIResponse(code=0, message="删除成功").model_dump()
