from fastapi import APIRouter
from app.services.payments.routes import router as payments_router

# API entrypoint for payments under /api/v1
router = APIRouter()
router.include_router(payments_router)
