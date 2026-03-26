from flask import Blueprint
from app.api.schemas import APIResponse

health_bp = Blueprint('health', __name__, url_prefix='/api')


@health_bp.route('/health', methods=['GET'])
def health_check():
    return APIResponse(
        code=0,
        message="success",
        data={"status": "healthy", "service": "SecuCert-Monitor"}
    ).model_dump()
