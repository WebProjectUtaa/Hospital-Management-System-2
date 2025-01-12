from unittest.mock import patch
import pytest
from login_service.main import app

@pytest.mark.asyncio
async def test_login_success():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Mocked notification sent"}

        async with app.asgi_client as client:
            payload = {"email": "admin2@example.com", "password": "admin2_password", "role": "admin"}
            request, response = await client.post("/login", json=payload)

            assert response.status == 200
            assert "access_token" in response.json
            assert "refresh_token" in response.json
            assert response.json["message"] == "Login successful"
