from sanic import Blueprint, response
from app.services.nurse_service import NurseService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware
import requests

# Mikroservis URL'leri
PATIENT_SERVICE_URL = "http://localhost:8001/patients"
NOTIFICATION_SERVICE_URL = "http://localhost:8000/notifications"

# Blueprint oluşturuluyor
nurse_bp = Blueprint("nurse_routes", url_prefix="/nurses")

@nurse_bp.get("/<nurse_id>/patients")
@auth_middleware
async def get_assigned_patients(request, nurse_id):
    """
    Belirli bir hemşireye atanmış hastaları döndür.
    """
    user = request.ctx.user
    if user["role"] != "nurse" or user["id"] != int(nurse_id):
        return response.json({"error": "Unauthorized access."}, status=403)

    async with await get_db_connection() as conn:
        try:
            patients = await NurseService.get_assigned_patients(conn, nurse_id)
            return response.json(patients, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@nurse_bp.post("/assign")
@auth_middleware
async def assign_patient(request):
    """
    Hemşireye yeni bir hasta ataması yap.
    Sadece admin yetkisine sahip kişiler bu işlemi yapabilir.
    """
    user = request.ctx.user
    if user["role"] != "admin":
        return response.json({"error": "Unauthorized access."}, status=403)

    data = request.json
    required_fields = ["nurse_id", "patient_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await NurseService.assign_patient(conn, data["nurse_id"], data["patient_id"])

            # Bildirim Gönderimi
            notification_data = {
                "to_email": await NurseService.get_patient_email(conn, data["patient_id"]),
                "subject": "New Nurse Assigned",
                "message": "You have been assigned a new nurse for your care."
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service error: {e}")

            return response.json(result, status=201)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@nurse_bp.put("/<nurse_id>/patients/<patient_id>/status")
@auth_middleware
async def update_patient_status(request, nurse_id, patient_id):
    """
    Hemşirenin hastanın durumunu güncellemesi.
    """
    user = request.ctx.user
    if user["role"] != "nurse" or user["id"] != int(nurse_id):
        return response.json({"error": "Unauthorized access."}, status=403)

    data = request.json
    required_fields = ["status", "notes"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await NurseService.update_patient_status(
                conn, patient_id, data["status"], data["notes"]
            )

            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@nurse_bp.get("/<nurse_id>/lab_tests")
@auth_middleware
async def get_lab_tests(request, nurse_id):
    """
    Hemşirenin sorumlu olduğu laboratuvar testlerini listele.
    """
    user = request.ctx.user
    if user["role"] != "nurse" or user["id"] != int(nurse_id):
        return response.json({"error": "Unauthorized access."}, status=403)

    async with await get_db_connection() as conn:
        try:
            lab_tests = await NurseService.get_lab_tests(conn, nurse_id)
            return response.json(lab_tests, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)
