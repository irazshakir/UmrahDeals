from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
import uuid

from app.db import models
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantOut


class TenantCRUD:
    @staticmethod
    def create(db: Session, tenant_in: TenantCreate) -> TenantOut:
        new_tenant = models.Tenant(
            tenant_name=tenant_in.tenant_name,
            tenant_email=tenant_in.tenant_email,
            tenant_phone=tenant_in.tenant_phone,
            tenant_address=tenant_in.tenant_address,
            plan_type=tenant_in.plan_type,
            subscription_status=tenant_in.subscription_status,
            trial_start_date=tenant_in.trial_start_date,
            trial_end_date=tenant_in.trial_end_date,
            subscription_start_date=tenant_in.subscription_start_date,
            subscription_end_date=tenant_in.subscription_end_date,
            max_users=tenant_in.max_users,
            max_storage_mb=tenant_in.max_storage_mb,
            api_rate_limit=tenant_in.api_rate_limit,
            notes=tenant_in.notes,
        )
        try:
            db.add(new_tenant)
            db.commit()
            db.refresh(new_tenant)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant with this name/email/phone already exists.",
            )
        # 🚀 TODO: publish event to auth-service to create admin user
        return new_tenant

    @staticmethod
    def get(db: Session, tenant_id: uuid.UUID) -> Optional[models.Tenant]:
        return db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[models.Tenant]:
        return db.query(models.Tenant).filter(models.Tenant.tenant_email == email).first()

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 50) -> List[models.Tenant]:
        return db.query(models.Tenant).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, tenant_id: uuid.UUID, tenant_in: TenantUpdate) -> Optional[models.Tenant]:
        tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

        update_data = tenant_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tenant, field, value)

        db.commit()
        db.refresh(tenant)
        return tenant

    @staticmethod
    def delete(db: Session, tenant_id: uuid.UUID) -> bool:
        tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

        db.delete(tenant)
        db.commit()
        return True
