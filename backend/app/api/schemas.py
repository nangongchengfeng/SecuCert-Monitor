from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class APIResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None


class CertificateCreate(BaseModel):
    service_name: Optional[str] = None
    use_deploy: Optional[str] = None
    deployA: Optional[str] = None
    deployB: Optional[str] = None
    product: Optional[str] = None
    scene: Optional[str] = None
    organ: Optional[str] = None
    manage: Optional[str] = None
    manage_id: Optional[str] = None
    issuance_date: Optional[str] = None
    expiration_date: Optional[str] = None
    header: Optional[str] = None
    tech: Optional[str] = None
    yumwei: Optional[str] = None
    yumwei_time: Optional[str] = None
    manager: Optional[str] = None
    type: str
    remark: Optional[str] = None


class CertificateUpdate(CertificateCreate):
    pass
