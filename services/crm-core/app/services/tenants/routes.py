from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantOut
from .crud import TenantCRUD

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=TenantOut, status_code=201)
def create_tenant(tenant_in: TenantCreate, db: Session = Depends(get_db)):
    return TenantCRUD.create(db=db, tenant_in=tenant_in)


@router.get("/{tenant_id}", response_model=TenantOut)
def get_tenant(tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    tenant = TenantCRUD.get(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.get("/", response_model=List[TenantOut])
def list_tenants(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return TenantCRUD.list(db=db, skip=skip, limit=limit)


@router.put("/{tenant_id}", response_model=TenantOut)
def update_tenant(tenant_id: uuid.UUID, tenant_in: TenantUpdate, db: Session = Depends(get_db)):
    return TenantCRUD.update(db=db, tenant_id=tenant_id, tenant_in=tenant_in)


@router.delete("/{tenant_id}", status_code=204)
def delete_tenant(tenant_id: uuid.UUID, db: Session = Depends(get_db)):
    TenantCRUD.delete(db=db, tenant_id=tenant_id)
    return {"ok": True}
