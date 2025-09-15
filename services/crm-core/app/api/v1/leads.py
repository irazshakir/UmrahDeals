# v1/: versioning your APIs (important for backward compatibility).

# leads.py → endpoints for leads (GET /leads, POST /leads)

# contacts.py → endpoints for contacts

# activities.py → endpoints for activities

# app/api/v1/leads.py
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.schemas.lead import LeadCreate, LeadRead
from app.services.lead_service import create_lead, list_leads

router = APIRouter()

# Simple tenant resolver via header (for demo)
async def get_tenant(x_tenant: Optional[str] = Header(None)):
    if not x_tenant:
        raise HTTPException(status_code=400, detail="X-Tenant header missing")
    return x_tenant

@router.post("/", response_model=LeadRead)
async def post_lead(payload: LeadCreate, db: AsyncSession = Depends(get_db), tenant: str = Depends(get_tenant)):
    return await create_lead(db, tenant, payload)

@router.get("/", response_model=List[LeadRead])
async def get_leads(db: AsyncSession = Depends(get_db), tenant: str = Depends(get_tenant)):
    leads = await list_leads(db, tenant)
    return leads
