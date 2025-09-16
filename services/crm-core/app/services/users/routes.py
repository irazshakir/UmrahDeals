from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from .crud import UserCRUD

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/tenant/{tenant_id}", response_model=UserOut, status_code=201)
def create_user(tenant_id: uuid.UUID, user_in: UserCreate, db: Session = Depends(get_db)):
    return UserCRUD.create(db=db, tenant_id=tenant_id, user_in=user_in)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = UserCRUD.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/tenant/{tenant_id}", response_model=List[UserOut])
def list_users(tenant_id: uuid.UUID, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return UserCRUD.list(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: uuid.UUID, user_in: UserUpdate, db: Session = Depends(get_db)):
    return UserCRUD.update(db=db, user_id=user_id, user_in=user_in)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    UserCRUD.delete(db=db, user_id=user_id)
    return {"ok": True}
