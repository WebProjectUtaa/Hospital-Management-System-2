from sanic import Blueprint, response
from app.services.patient_service import PatientService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware
import requests

patient_bp = Blueprint("patient_routes", url_prefix="/patients")

# Diğer mikroservislerin URL'leri
LAB_TEST_SERVICE_URL = "http://localhost:8002/lab_tests"
PRESCRIPTION_SERVICE_URL = "http://localhost:8003/prescriptions"
APPOINTMENT_SERVICE_URL = "http://localhost:8004/appointments"
NOTIFICATION_SERVICE_URL = "http://localhost:8000/notifications"

@patient_bp.get("/<patient_id>")
@auth_middleware
async def get_patient_details(request, patient_id):
    """
    Hastanın detaylarını getir.
    """
    async with await get_db_connection() as conn:
        try:
            patient = await PatientService.get_patient_details(conn, patient_id)
            return response.json(patient, status=200)
        except ValueError as e:
            return response.json({"error": str(e)}, status=404)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@patient_bp.get("/<patient_id>/medical_history")
@auth_middleware
async def get_medical_history(request, patient_id):
    """
    Hastanın tıbbi geçmişini getir.
    """
    try:
        # Randevu geçmişini al
        appointment_response = requests.get(f"{APPOINTMENT_SERVICE_URL}/{patient_id}/history")
        appointments = appointment_response.json() if appointment_response.status_code == 200 else []

        # Laboratuvar testlerini al
        lab_test_response = requests.get(f"{LAB_TEST_SERVICE_URL}/{patient_id}")
        lab_tests = lab_test_response.json() if lab_test_response.status_code == 200 else []

        # Reçeteleri al
        prescription_response = requests.get(f"{PRESCRIPTION_SERVICE_URL}/{patient_id}")
        prescriptions = prescription_response.json() if prescription_response.status_code == 200 else []

        # Tıbbi geçmişi birleştir
        medical_history = {
            "appointments": appointments,
            "lab_tests": lab_tests,
            "prescriptions": prescriptions
        }

        return response.json(medical_history, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.get("/<patient_id>/lab_tests")
@auth_middleware
async def get_lab_tests(request, patient_id):
    """
    Hastanın laboratuvar testlerini getir.
    """
    try:
        lab_test_response = requests.get(f"{LAB_TEST_SERVICE_URL}/{patient_id}")
        if lab_test_response.status_code == 200:
            return response.json(lab_test_response.json(), status=200)
        return response.json({"error": "Failed to fetch lab tests"}, status=500)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.get("/<patient_id>/prescriptions")
@auth_middleware
async def get_prescriptions(request, patient_id):
    """
    Hastanın reçetelerini getir.
    """
    try:
        prescription_response = requests.get(f"{PRESCRIPTION_SERVICE_URL}/{patient_id}")
        if prescription_response.status_code == 200:
            return response.json(prescription_response.json(), status=200)
        return response.json({"error": "Failed to fetch prescriptions"}, status=500)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.post("/<patient_id>/notifications")
@auth_middleware
async def send_notification(request, patient_id):
    """
    Hastaya bildirim gönder.
    """
    data = request.json
    required_fields = ["subject", "message"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    try:
        notification_data = {
            "to_email": data.get("to_email"),
            "subject": data["subject"],
            "message": data["message"]
        }
        notification_response = requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)

        if notification_response.status_code == 200:
            return response.json({"message": "Notification sent successfully"}, status=200)
        return response.json({"error": "Failed to send notification"}, status=500)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)