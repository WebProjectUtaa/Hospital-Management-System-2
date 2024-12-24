from sanic import Blueprint, response
from app.services.login_service import LoginService
from app.db.init_db import get_db_connection
from utils.hash_utils import verify_password

login_bp = Blueprint("login")

@login_bp.post("/login")
async def login(request):
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    async with get_db_connection() as conn:
        if role:
            user = await LoginService.authenticate_user(conn, email, password, role)
        else:
            user = await LoginService.authenticate_patient(conn, email, password)

        if user:
            return response.json({"message": "Login successful", "user": user})
        return response.json({"message": "Invalid credentials"}, status=401)
