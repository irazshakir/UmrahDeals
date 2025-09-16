from fastapi import APIRouter
from app.services.auth.routes import router as auth_router

# API entrypoint for auth under /api/v1/auth
router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
