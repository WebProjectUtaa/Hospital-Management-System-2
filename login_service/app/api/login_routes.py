from sanic import Blueprint, response
from app.services.login_service import LoginService
from app.db.init_db import get_db_connection
from utils.jwt_utils import create_token
from dotenv import load_dotenv
import os

# Çevresel değişkenleri yükle
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

login_bp = Blueprint("login_routes", url_prefix="/login")

@login_bp.post("/")
async def login(request):
    """
    Kullanıcı login işlemi için route.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", None)

    if not email or not password:
        return response.json({"error": "Email and password are required"}, status=400)

    async with await get_db_connection() as conn:
        try:
            # Kullanıcı kimlik doğrulama
            user = await LoginService.authenticate_user(conn, email, password, role)
            if user:
                # Kullanıcı doğrulandıysa JWT token oluştur
                token = create_token({"id": user["id"], "email": user["email"], "role": user["role"]}, SECRET_KEY)
                return response.json({"message": "Login successful", "token": token}, status=200)
            else:
                return response.json({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)
