import pytest
from httpx import AsyncClient
from app.main import app
import uuid

@pytest.mark.asyncio
async def test_signup():
    email = f"testuser_{uuid.uuid4()}@example.com"
    payload = {
        "email": email,
        "password": "TestPassword123!",
        "role": "ops"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/auth/signup", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "verification_url" in data
    # Save for next test
    test_signup.email = email
    test_signup.verification_url = data["verification_url"]

@pytest.mark.asyncio
async def test_email_verification():
    # Use the verification_url from signup
    verification_url = getattr(test_signup, "verification_url", None)
    assert verification_url is not None
    # Extract token from URL
    token = verification_url.split("/")[-1]
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/auth/verify-email/{token}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Email verified successfully"

@pytest.mark.asyncio
async def test_login():
    email = getattr(test_signup, "email", None)
    assert email is not None
    payload = {
        "email": email,
        "password": "TestPassword123!",
        "role": "ops"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
