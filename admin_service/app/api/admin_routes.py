from sanic import Blueprint, response
from app.services.admin_service import AdminService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware
import requests

# Mikroservis URL'leri
PATIENT_SERVICE_URL = "http://localhost:8001/patients"
DOCTOR_SERVICE_URL = "http://localhost:8002/doctors"
NURSE_SERVICE_URL = "http://localhost:8003/nurses"
LAB_TEST_SERVICE_URL = "http://localhost:8004/lab_tests"
APPOINTMENT_SERVICE_URL = "http://localhost:8005/appointments"
NOTIFICATION_SERVICE_URL = "http://localhost:8000/notifications"

# Blueprint oluşturuluyor
admin_bp = Blueprint("admin_routes", url_prefix="/admin")

@admin_bp.get("/users")
@auth_middleware
async def list_users(request):
    """
    Tüm kullanıcıları listele.
    """
    async with await get_db_connection() as conn:
        try:
            users = await AdminService.get_all_users(conn)
            return response.json(users, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.post("/users")
@auth_middleware
async def add_user(request):
    """
    Yeni bir kullanıcı ekle.
    """
    data = request.json
    required_fields = ["name", "surname", "role", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await AdminService.add_user(conn, data)
            return response.json(result, status=201)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.put("/users/<user_id:int>")
@auth_middleware
async def update_user(request, user_id):
    """
    Kullanıcı bilgilerini güncelle.
    """
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update."}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await AdminService.update_user(conn, user_id, data)
            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.delete("/users/<user_id:int>")
@auth_middleware
async def delete_user(request, user_id):
    """
    Kullanıcıyı sil.
    """
    async with await get_db_connection() as conn:
        try:
            result = await AdminService.delete_user(conn, user_id)
            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.get("/departments")
@auth_middleware
async def list_departments(request):
    """
    Tüm departmanları listele.
    """
    async with await get_db_connection() as conn:
        try:
            departments = await AdminService.get_all_departments(conn)
            return response.json(departments, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.post("/departments")
@auth_middleware
async def add_department(request):
    """
    Yeni bir departman ekle.
    """
    data = request.json
    required_fields = ["department_name"]
    if "department_name" not in data:
        return response.json({"error": "Missing field: department_name"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await AdminService.add_department(conn, data["department_name"])
            return response.json(result, status=201)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.put("/departments/<department_id:int>")
@auth_middleware
async def update_department(request, department_id):
    """
    Departman bilgilerini güncelle.
    """
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update."}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await AdminService.update_department(conn, department_id, data)
            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@admin_bp.delete("/departments/<department_id:int>")
@auth_middleware
async def delete_department(request, department_id):
    """
    Departmanı sil.
    """
    async with await get_db_connection() as conn:
        try:
            result = await AdminService.delete_department(conn, department_id)
            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

# Daha fazla endpoint diğer requirement'lar için benzer şekilde eklenebilir.
