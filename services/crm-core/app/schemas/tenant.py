from pydantic import BaseModel, EmailStr, constr
from typing import Annotated, Optional
from uuid import UUID
from datetime import datetime, date
from enum import Enum

# Import your enums (same as in models)
from app.db.models import PlanType, SubscriptionStatus


TenantName = Annotated[str, constr(strip_whitespace=True, min_length=2, max_length=100)]


# -------- BASE SCHEMA -------- #
class TenantBase(BaseModel):
    tenant_name: Optional[TenantName] = None
    tenant_email: EmailStr
    tenant_phone: Optional[str] = None
    tenant_address: Optional[str] = None

    plan_type: Optional[PlanType] = PlanType.free
    subscription_status: Optional[SubscriptionStatus] = SubscriptionStatus.trialing

    trial_start_date: Optional[date] = None
    trial_end_date: Optional[date] = None
    subscription_start_date: Optional[date] = None
    subscription_end_date: Optional[date] = None

    max_users: Optional[int] = 5
    max_storage_mb: Optional[int] = 100
    api_rate_limit: Optional[int] = 1000

    notes: Optional[str] = None
    is_active: Optional[bool] = True
    is_suspended: Optional[bool] = False


# -------- CREATE -------- #
class TenantCreate(TenantBase):
    tenant_name: Optional[TenantName] = None
    tenant_email: EmailStr


# -------- UPDATE -------- #
class TenantUpdate(BaseModel):
    tenant_name: Optional[TenantName] = None
    tenant_email: Optional[EmailStr] = None
    tenant_phone: Optional[str] = None
    tenant_address: Optional[str] = None

    plan_type: Optional[PlanType] = None
    subscription_status: Optional[SubscriptionStatus] = None

    trial_start_date: Optional[date] = None
    trial_end_date: Optional[date] = None
    subscription_start_date: Optional[date] = None
    subscription_end_date: Optional[date] = None

    max_users: Optional[int] = None
    max_storage_mb: Optional[int] = None
    api_rate_limit: Optional[int] = None

    notes: Optional[str] = None
    is_active: Optional[bool] = None
    is_suspended: Optional[bool] = None


# -------- READ/OUTPUT -------- #
class TenantOut(TenantBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ allows SQLAlchemy models → Pydantic conversion
