from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class UserRoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


# Shared
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    role: UserRoleEnum = UserRoleEnum.staff
    is_active: bool = True


# Create
class UserCreate(UserBase):
    password: str  # plain password, will hash in CRUD


# Update
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    is_active: Optional[bool] = None


# Output
class UserOut(UserBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
