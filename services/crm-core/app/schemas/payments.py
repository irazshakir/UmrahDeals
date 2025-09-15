from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime


# ------------------------------
# Base schema (shared fields)
# ------------------------------
class PaymentBase(BaseModel):
    tenant_id: UUID
    amount: float = Field(..., gt=0, description="Payment amount must be greater than 0")
    currency: str = Field(default="USD", max_length=3, description="Currency code (ISO 4217)")
    status: Literal["paid", "unpaid", "pending"] = "pending"
    payment_due_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None


# ------------------------------
# Schema for creating a payment
# ------------------------------
class PaymentCreate(PaymentBase):
    pass


# ------------------------------
# Schema for updating a payment
# ------------------------------
class PaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=3)
    status: Optional[Literal["paid", "unpaid", "pending"]] = None
    payment_due_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None


# ------------------------------
# Schema for reading/response
# ------------------------------
class PaymentResponse(PaymentBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

