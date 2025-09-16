from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth

app = FastAPI(title="auth-service")

# CORS (allow local frontend during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned routes
app.include_router(auth.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
