from sanic import response
from utils.jwt_utils import verify_token
from dotenv import load_dotenv
import os

# Çevresel değişkenleri yükle
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

async def auth_middleware(request):
    """
    JWT doğrulama middleware'i.
    """
    token = request.headers.get("Authorization")
    if not token:
        return response.json({"error": "Authorization token is missing"}, status=401)
    
    token = token.replace("Bearer ", "")  # "Bearer " kısmını temizle
    try:
        decoded_token = verify_token(token, SECRET_KEY)
        request.ctx.user = decoded_token  # Doğrulanan kullanıcıyı request'e ekle
    except RuntimeError as e:
        return response.json({"error": str(e)}, status=401)
