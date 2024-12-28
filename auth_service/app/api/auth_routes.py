from sanic import Blueprint, response
from app.services.auth_service import AuthService
from app.db.init_db import get_db_connection
from utils.jwt_utils import verify_token, create_token
from dotenv import load_dotenv
import os
import requests

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
AUTH_SERVICE_URL = "http://localhost:8000/auth"

auth_bp = Blueprint("auth_routes", url_prefix="/auth")

@auth_bp.get("/select")
async def select_role(request):
    """
    Kullanıcının rol seçimi için endpoint.
    """
    roles = ["patient", "doctor", "admin", "nurse"]  # Desteklenen roller
    return response.json({"roles": roles}, status=200)

@auth_bp.get("/login/<role>")
async def role_based_login(request, role):
    """
    Rol bazlı login ekranına yönlendirme.
    """
    if role not in ["patient", "doctor", "admin", "nurse"]:
        return response.json({"error": "Invalid role selected"}, status=400)
    return response.json({"message": f"Login screen for {role}"}, status=200)

@auth_bp.post("/login")
async def login(request):
    """
    Genel kimlik doğrulama işlemi.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password or not role:
        return response.json({"error": "Email, password, and role are required"}, status=400)

    try:
        async with await get_db_connection() as conn:
            if role == "patient":
                result = await AuthService.authenticate_patient(conn, email, password)
            else:
                result = await AuthService.authenticate_employee(conn, email, password)

            if "error" in result:
                return response.json(result, status=401)

            # Token üretme ve REST çağrısı
            headers = {"Authorization": f"Bearer {result['token']}"}
            try:
                rest_call = requests.post(
                    f"{AUTH_SERVICE_URL}/validate_token",
                    headers=headers
                )
                if rest_call.status_code != 200:
                    return response.json({"error": "Token validation failed"}, status=401)
            except Exception as rest_error:
                return response.json({"error": f"REST call failed: {rest_error}"}, status=500)

            return response.json({"message": "Login successful", "data": result}, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@auth_bp.post("/validate_token")
async def validate_token(request):
    """
    Token doğrulama endpoint'i.
    """
    token = request.json.get("token")
    if not token:
        return response.json({"error": "Token is missing"}, status=400)

    try:
        decoded = verify_token(token, SECRET_KEY)
        return response.json({"message": "Token is valid", "data": decoded}, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=401)

@auth_bp.post("/refresh_token")
async def refresh_token(request):
    """
    Refresh token kullanarak yeni bir access token oluşturur.
    """
    # İstekten refresh token'i al
    refresh_token = request.json.get("refresh_token")
    if not refresh_token:
        return response.json({"error": "Refresh token is missing"}, status=400)

    try:
        # Token doğrulama
        decoded = verify_token(refresh_token, SECRET_KEY)

        # Yeni access token oluştur
        access_token = create_token({
            "id": decoded["id"],
            "email": decoded["email"],
            "role": decoded["role"]
        }, SECRET_KEY, expires_in=900)  # 15 dakikalık yeni access token

        return response.json({"access_token": access_token}, status=200)

    except Exception as e:
        # Hata durumunda kullanıcıya bilgi gönder
        return response.json({"error": str(e)}, status=401)
