import pytest
from login_service.main import app

@pytest.mark.asyncio
async def test_login_success():
    """
    Başarılı giriş testi.
    """
    async with app.asgi_client as client:
        payload = {"email": "admin2@example.com", "password": "admin2_password", "role": "admin"}
        request, response = await client.post("/login", json=payload)

        # Assertion kontrolleri
        assert response.status == 200
        assert "access_token" in response.json
        assert "refresh_token" in response.json
        assert response.json["message"] == "Login successful"


@pytest.mark.asyncio
async def test_login_failure_wrong_password():
    """
    Hatalı şifre ile giriş testi.
    """
    async with app.asgi_client as client:
        payload = {"email": "admin@example.com", "password": "wrong_password", "role": "admin"}
        request, response = await client.post("/login", json=payload)

        # Assertion kontrolleri
        assert response.status == 401
        assert response.json["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_failure_missing_fields():
    """
    Eksik bilgi ile giriş testi.
    """
    async with app.asgi_client as client:
        payload = {"email": "admin2@example.com"}  # Şifre eksik
        request, response = await client.post("/login", json=payload)

        # Assertion kontrolleri
        assert response.status == 400
        assert response.json["error"] == "Missing required fields"


@pytest.mark.asyncio
async def test_login_failure_invalid_user():
    """
    Geçersiz kullanıcı girişi testi.
    """
    async with app.asgi_client as client:
        payload = {"email": "unknown@example.com", "password": "password123", "role": "admin"}
        request, response = await client.post("/login", json=payload)

        # Assertion kontrolleri
        assert response.status == 404
        assert response.json["message"] == "User not found"
