from sanic import Blueprint, response
from app.services.patient_service import PatientService
from app.db.init_db import get_db_connection
from app.api.auth import role_required
import requests

NOTIFICATION_SERVICE_URL = "http://localhost:8000/notifications"
PATIENT_BP_PREFIX = "/patients"

patient_bp = Blueprint("patient", url_prefix=PATIENT_BP_PREFIX)

@patient_bp.post("/", name="add_patient")
@role_required(["receptionist"])
async def add_patient(request):
    """
    Yeni hasta eklemek için route.
    """
    data = request.json
    required_fields = ["name", "surname", "age", "blood_group", "gender", "contacts", "keen_contacts", "insurance", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

    try:
        async with await get_db_connection() as conn:
            result = await PatientService.add_patient(conn, **data)

            # Notification Service entegrasyonu
            notification_data = {
                "to_email": data["email"],
                "subject": "Welcome to Hospital Management System",
                "message": f"Dear {data['name']} {data['surname']},\n\nYou have been successfully registered as a patient.\n\nBest regards,\nHospital Management System"
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service error: {e}")

            return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.get("/", name="get_all_patients")
@role_required(["receptionist", "admin"])
async def get_all_patients(request):
    """
    Tüm hastaları listelemek için route.
    """
    try:
        async with await get_db_connection() as conn:
            patients = await PatientService.get_all_patients(conn)
            return response.json(patients, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.put("/<patient_id:int>", name="update_patient")
@role_required(["receptionist"])
async def update_patient(request, patient_id):
    """
    Hasta bilgilerini güncellemek için route.
    """
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update"}, status=400)

    try:
        async with await get_db_connection() as conn:
            result = await PatientService.update_patient(conn, patient_id, data)

            # Güncelleme durumunda bildirim gönderme
            if "email" in data:
                notification_data = {
                    "to_email": data["email"],
                    "subject": "Patient Information Updated",
                    "message": "Your patient information has been successfully updated."
                }
                try:
                    requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
                except Exception as e:
                    print(f"Notification Service error: {e}")

            return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.delete("/<patient_id:int>", name="delete_patient")
@role_required(["receptionist"])
async def delete_patient(request, patient_id):
    """
    Hasta kaydını silmek için route.
    """
    try:
        async with await get_db_connection() as conn:
            result = await PatientService.delete_patient(conn, patient_id)

            # Hasta silinmesi durumunda bildirim gönderme
            notification_data = {
                "to_email": "admin@hospital.com",
                "subject": "Patient Record Deleted",
                "message": f"The patient record with ID {patient_id} has been deleted."
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service error: {e}")

            return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
