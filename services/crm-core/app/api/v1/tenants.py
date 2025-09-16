from fastapi import APIRouter
from app.services.tenants.routes import router as tenants_router

# This is the API entrypoint for tenants under /api/v1
router = APIRouter()
router.include_router(tenants_router)
