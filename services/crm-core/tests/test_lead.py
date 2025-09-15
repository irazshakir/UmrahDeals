# Pytest-based tests.

# test_leads.py: unit + integration tests for leads.

# tests/test_leads.py (very minimal, uses httpx AsyncClient)
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
