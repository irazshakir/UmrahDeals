import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import Index
import enum



class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    name = Column(String, nullable=False)
    phone = Column(String, nullable=True, unique=True)

    role = Column(Enum(UserRoleEnum, name="user_role_enum"), default=UserRoleEnum.user, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", backref="users")

    __table_args__ = (
        # Queries like: fetch all users for a tenant
        Index("ix_users_tenant_id", "tenant_id"),
        # Queries like: fetch active users for a tenant
        Index("ix_users_tenant_active", "tenant_id", "is_active"),
        # Queries like: fetch users by role within a tenant
        Index("ix_users_tenant_role", "tenant_id", "role"),
    )