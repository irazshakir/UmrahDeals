# tenancy.py → Tenant middleware (resolves tenant_id from header/domain).

from fastapi import Request, Depends

def get_tenant(request: Request) -> str:
    return request.headers.get("X-Tenant-ID")
