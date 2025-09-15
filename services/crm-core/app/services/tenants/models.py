import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Enum,
    Integer,
    Text,
    Date,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


# -------- ENUM CLASSES -------- #
class PlanType(enum.Enum):
    free = "free"
    monthly = "monthly"
    quarterly = "quarterly"
    yearly = "yearly"


class SubscriptionStatus(enum.Enum):
    trialing = "trialing"
    active = "active"
    cancelled = "cancelled"
    expired = "expired"
    grace_period = "grace_period"


# -------- TENANT MODEL -------- #
class Tenant(Base):
    __tablename__ = "tenants"

    # Core Identity
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_name = Column(String, nullable=False, unique=True, index=True)
    tenant_email = Column(String, nullable=False, unique=True, index=True)
    tenant_phone = Column(String, nullable=True, unique=True)
    tenant_address = Column(String, nullable=True)

    # Lifecycle Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Subscription Management
    plan_type = Column(Enum(PlanType), default=PlanType.free, nullable=False, index=True)
    subscription_status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.trialing, nullable=False, index=True)

    trial_start_date = Column(Date, nullable=True)
    trial_end_date = Column(Date, nullable=True)
    subscription_start_date = Column(Date, nullable=True)
    subscription_end_date = Column(Date, nullable=True)

    # Feature Limits
    max_users = Column(Integer, default=5, nullable=False)
    max_storage_mb = Column(Integer, default=100, nullable=False)
    api_rate_limit = Column(Integer, default=1000, nullable=False)

    # Status & Notes
    is_active = Column(Boolean, default=True, nullable=False)
    is_suspended = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)

    # Indexes
    __table_args__ = (
        # Queries like: find all tenants with active plan
        Index("ix_tenants_plan_status", "plan_type", "subscription_status"),
        # Queries like: quickly check active vs suspended tenants
        Index("ix_tenants_active_suspended", "is_active", "is_suspended"),
    )
