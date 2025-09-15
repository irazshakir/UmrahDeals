# Pydantic models (input/output validation).

# lead.py → LeadCreate, LeadRead, LeadUpdate.

# contact.py, activity.py → same pattern.

# These are used in API routes to validate request bodies and responses.

# app/schemas/lead.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    name: str
    email: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadRead(LeadBase):
    id: int
    tenant_id: str
    created_at: datetime

    class Config:
        orm_mode = True
