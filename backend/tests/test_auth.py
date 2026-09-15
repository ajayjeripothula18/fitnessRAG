import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    # Register once
    await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "securepassword123"},
    )
    # Register again with same email
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "securepassword123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "loginuser@example.com", "password": "mypassword123"},
    )
    # Login via OAuth2 form data
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser@example.com", "password": "mypassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpwd@example.com", "password": "correctpassword"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpwd@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_get_current_user_me(client: AsyncClient):
    # Register & login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "meuser@example.com", "password": "mypassword123"},
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "meuser@example.com", "password": "mypassword123"},
    )
    token = login_resp.json()["access_token"]

    # Request /me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "meuser@example.com"
