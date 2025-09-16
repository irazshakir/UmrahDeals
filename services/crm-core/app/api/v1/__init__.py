from fastapi import APIRouter
from . import tenants, users, payments

api_router = APIRouter()
api_router.include_router(tenants.router)
api_router.include_router(users.router)
api_router.include_router(payments.router)