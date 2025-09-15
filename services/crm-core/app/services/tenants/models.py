import uuid 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean
from app.db.base import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_name = Column(String, nullable=False, unique=True)
    tenant_is_active = Column(Boolean, default=True, nullable=False)
    tenant_email = Column(String, nullable=False, unique=True)
    tenant_phone = Column(String, nullable=True, unique=True)
    tenant_address = Column(String, nullable=True)

    