# App initialization

# Middleware (CORS, logging, tenancy)

# Router registration (api/v1/leads, etc)

# app/main.py
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.v1 import leads
from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(title="crm-core")

# CORS (allow local frontend during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(leads.router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
