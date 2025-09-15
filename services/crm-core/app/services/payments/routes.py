from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas import payments as schemas
from . import crud

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db, payment.dict())


@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: UUID, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.get("/tenant/{tenant_id}", response_model=list[schemas.PaymentResponse])
def get_payments_by_tenant(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_payments_by_tenant(db, tenant_id, skip=skip, limit=limit)


@router.put("/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(
    payment_id: UUID,
    update_data: schemas.PaymentUpdate,
    db: Session = Depends(get_db)
):
    updated_payment = crud.update_payment(db, payment_id, update_data.dict(exclude_unset=True))
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


@router.delete("/{payment_id}", response_model=dict)
def delete_payment(payment_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_payment(db, payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}


