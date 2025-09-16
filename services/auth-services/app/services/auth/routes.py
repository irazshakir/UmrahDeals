from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token, verify_password
from app.db.models import User  # referencing the shared Users table
from datetime import timedelta
from fastapi import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

# Define your JWT secret key and algorithm
SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Fetch user
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Include extra fields in token
    token_data = {
        "sub": user.email,
        "tenant_id": user.tenant_id,
        "role": user.role,
        "name": user.name
    }

    access_token = create_access_token(token_data)
    refresh_token = create_access_token(token_data)  # you could make expiry longer here

    # Return tokens + user info for frontend storage
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role,
        "tenant_id": user.tenant_id,
        "name": user.name
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.auth_jwt_secret, algorithms=[settings.auth_jwt_algorithm])
        email: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        role: str = payload.get("role")
        name: str = payload.get("name")

        if email is None or tenant_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Generate new access token
    new_token_data = {
        "sub": email,
        "tenant_id": tenant_id,
        "role": role,
        "name": name,
    }
    access_token = create_access_token(
        new_token_data,
        expires_delta=timedelta(minutes=settings.auth_access_token_expire_minutes),
    )

    return {
        "access_token": access_token,
        "refresh_token": token,
        "token_type": "bearer",
        "role": role,
        "tenant_id": tenant_id,
        "name": name,
    }

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    In JWT-based auth, logout is usually handled on the client by deleting tokens.
    For MVP, we just acknowledge the logout.
    Later, you can implement a token blacklist in Redis for refresh tokens.
    """
    return {
        "message": "Successfully logged out. Please remove tokens from client storage.",
        "access_token": None,
        "refresh_token": None,
        "role": None,
        "tenant_id": None,
        "name": None
    }


