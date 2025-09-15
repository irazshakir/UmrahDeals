from sqlalchemy import Column, String, ForeignKey, DateTime, Enum, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.db.base import Base


class PaymentGateway(enum.Enum):
    stripe = "stripe"
    paypal = "paypal"
    manual = "manual"  # for offline payments


class TransactionStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="USD", nullable=False)

    gateway = Column(Enum(PaymentGateway), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.pending, nullable=False, index=True)

    transaction_reference = Column(String, nullable=True, unique=True)  # from Stripe/PayPal
    invoice_id = Column(String, nullable=True)  # optional link to invoices

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text, nullable=True)
