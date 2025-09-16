from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": user.email, "tenant_id": user.tenant_id}
    access_token = create_access_token(token_data)
    refresh_token = create_access_token(token_data)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        if email is None or tenant_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_token_data = {"sub": email, "tenant_id": tenant_id}
    access_token = create_access_token(new_token_data, expires_delta=timedelta(minutes=30))

    return {"access_token": access_token, "refresh_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out (delete token client-side)"}

