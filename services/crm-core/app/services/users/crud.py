from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid
from app.schemas.user import UserCreate, UserUpdate
from app.services.users.models import User
from app.core.security import get_password_hash  # assuming you already have this


class UserCRUD:
    @staticmethod
    def create(db: Session, tenant_id: uuid.UUID, user_in: UserCreate) -> User:
        new_user = User(
            tenant_id=tenant_id,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            name=user_in.name,
            phone=user_in.phone,
            role=user_in.role,
            is_active=user_in.is_active,
        )
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email/phone already exists.",
            )
        return new_user

    @staticmethod
    def get(db: Session, user_id: uuid.UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def list(db: Session, tenant_id: uuid.UUID, skip: int = 0, limit: int = 50):
        return db.query(User).filter(User.tenant_id == tenant_id).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: uuid.UUID) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return True
