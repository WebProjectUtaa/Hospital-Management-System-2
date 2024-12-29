from sanic import Blueprint, response
from app.services.lab_test_service import LabTestService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware
import requests

NOTIFICATION_SERVICE_URL = "http://localhost:8000/notifications"

lab_test_bp = Blueprint("lab_tests", url_prefix="/lab_tests")

@lab_test_bp.post("/")
@auth_middleware
async def create_lab_test(request):
    """
    Yeni bir laboratuvar testi oluştur.
    Sadece doktorlar tarafından kullanılabilir.
    """
    user = request.ctx.user
    if user["role"] != "doctor":
        return response.json({"error": "Only doctors can create lab tests."}, status=403)

    data = request.json
    required_fields = ["patient_id", "test_name", "priority"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with get_db_connection() as conn:
        try:
            # Test oluştur
            result = await LabTestService.create_lab_test(
                conn,
                data["patient_id"],
                user["id"],  # doctor_id
                data["test_name"],
                data["priority"],
                data.get("test_reason")
            )

            # Bildirim Gönderimi
            notification_data = {
                "to_email": await LabTestService.get_patient_email_by_test(conn, data["patient_id"]),
                "subject": "New Lab Test Requested",
                "message": f"A new lab test '{data['test_name']}' has been requested for you."
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service Error: {e}")

            return response.json(result, status=201)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@lab_test_bp.put("/<test_id:int>/status")
@auth_middleware
async def update_lab_test_status(request, test_id):
    """
    Laboratuvar testinin durumunu güncelle.
    Sadece lab_staff rolüne sahip kişiler bu işlemi yapabilir.
    """
    user = request.ctx.user
    if user["role"] != "lab_staff":
        return response.json({"error": "Unauthorized access."}, status=403)

    data = request.json
    if "status" not in data:
        return response.json({"error": "Missing field: status"}, status=400)

    async with get_db_connection() as conn:
        try:
            # Test durumunu güncelle
            result = await LabTestService.update_lab_test_status(
                conn, test_id, data["status"], data.get("result")
            )

            # Bildirim Gönderimi
            patient_email = await LabTestService.get_patient_email_by_test(conn, test_id)
            doctor_email = await LabTestService.get_doctor_email_by_test(conn, test_id)
            notification_data = {
                "to_email": [patient_email, doctor_email],
                "subject": "Lab Test Status Updated",
                "message": f"The lab test with ID {test_id} has been updated to '{data['status']}'."
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service Error: {e}")

            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@lab_test_bp.delete("/<test_id:int>")
@auth_middleware
async def delete_lab_test(request, test_id):
    """
    Laboratuvar testini sil.
    Sadece admin yetkisine sahip kişiler bu işlemi yapabilir.
    """
    user = request.ctx.user
    if user["role"] != "admin":
        return response.json({"error": "Unauthorized access."}, status=403)

    async with get_db_connection() as conn:
        try:
            result = await LabTestService.delete_lab_test(conn, test_id)
            return response.json(result, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)
