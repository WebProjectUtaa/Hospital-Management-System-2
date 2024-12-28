from sanic import Blueprint, response
from app.services.login_service import LoginService
from app.db.init_db import get_db_connection
from utils.jwt_utils import create_token
from dotenv import load_dotenv
import os
import jwt

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
                # Kullanıcı doğrulandıysa Access ve Refresh token oluştur
                access_token = create_token({"id": user["id"], "email": user["email"], "role": user["role"]}, SECRET_KEY, expires_in=9000)
                refresh_token = create_token({"id": user["id"]}, SECRET_KEY, expires_in=604800)
                return response.json({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, status=200)
            else:
                return response.json({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@login_bp.post("/refresh")
async def refresh_token(request):
    """
    Refresh token ile yeni access token oluştur.
    """
    data = request.json
    refresh_token = data.get("refresh_token")

    try:
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token["id"]
        # Yeni access token oluştur
        access_token = create_token({"id": user_id}, SECRET_KEY, expires_in=9000)
        return response.json({"access_token": access_token}, status=200)
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Refresh token expired"}, status=401)
    except jwt.InvalidTokenError:
        return response.json({"error": "Invalid token"}, status=401)
