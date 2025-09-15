from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from .models import Payment


def create_payment(db: Session, payment_data: dict) -> Payment:
    """Create a new payment record."""
    payment = Payment(**payment_data)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: UUID) -> Payment | None:
    """Fetch a payment by ID."""
    return db.get(Payment, payment_id)


def get_payments_by_tenant(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100) -> list[Payment]:
    """Fetch all payments for a given tenant."""
    stmt = select(Payment).where(Payment.tenant_id == tenant_id).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def update_payment(db: Session, payment_id: UUID, update_data: dict) -> Payment | None:
    """Update an existing payment."""
    payment = db.get(Payment, payment_id)
    if not payment:
        return None

    for key, value in update_data.items():
        setattr(payment, key, value)

    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


def delete_payment(db: Session, payment_id: UUID) -> bool:
    """Delete a payment by ID."""
    payment = db.get(Payment, payment_id)
    if not payment:
        return False

    db.delete(payment)
    db.commit()
    return True
