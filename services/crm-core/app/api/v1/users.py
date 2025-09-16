# v1/: versioning your APIs (important for backward compatibility).

from fastapi import APIRouter
from app.services.users.routes import router as users_router

# API entrypoint for users under /api/v1
router = APIRouter()
router.include_router(users_router)
