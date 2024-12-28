from sanic import Blueprint, response
from app.services.auth_service import AuthService
from app.db.init_db import get_db_connection
from utils.jwt_utils import verify_token
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
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

    # Veritabanı işlemleri
    async with await get_db_connection() as conn:
        try:
            if role == "patient":
                result = await AuthService.authenticate_patient(conn, email, password)
            else:
                result = await AuthService.authenticate_employee(conn, email, password)

            if "error" in result:
                return response.json(result, status=401)

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