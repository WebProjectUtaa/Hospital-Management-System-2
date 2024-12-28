import requests
from sanic import response
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")  # Auth Service URL

async def auth_middleware(request):
    """
    Token doğrulama middleware'i.
    """
    # Authorization header'dan token'ı al
    token = request.headers.get("Authorization")
    if not token:
        return response.json({"error": "Missing Authorization header"}, status=401)
    
    token = token.replace("Bearer ", "")  # "Bearer " kısmını temizle

    try:
        # Auth Service'e token doğrulama isteği gönder
        auth_response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/validate_token",
            json={"token": token}
        )

        # Eğer doğrulama başarılıysa
        if auth_response.status_code == 200:
            request.ctx.user = auth_response.json()["data"]  # Kullanıcı bilgilerini request'e ekle
        else:
            return response.json({"error": "Invalid token"}, status=401)

    except Exception as e:
        return response.json({"error": f"Failed to validate token: {e}"}, status=500)
