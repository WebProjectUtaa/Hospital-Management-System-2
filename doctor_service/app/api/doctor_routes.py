from sanic import Blueprint, response
from app.services.doctor_service import DoctorService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware
from dotenv import load_dotenv
import os
import requests

# Blueprint oluşturuluyor
doctor_bp = Blueprint("doctor_routes", url_prefix="/doctors")

# Environment variables yükleniyor
load_dotenv()
LAB_TEST_SERVICE_URL = os.getenv("LAB_TEST_SERVICE_URL", "http://localhost:8002/lab_tests")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8000/notifications")

@doctor_bp.get("/<doctor_id>/appointments")
@auth_middleware
async def get_appointments(request, doctor_id):
    """
    Belirli bir doktorun tüm randevularını döner.
    """
    user = request.ctx.user  # Middleware tarafından sağlanan kullanıcı verisi
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    async with await get_db_connection() as conn:
        try:
            appointments = await DoctorService.get_appointments(conn, doctor_id)
            return response.json({"appointments": appointments}, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@doctor_bp.get("/<doctor_id>/patients")
@auth_middleware
async def get_patients(request, doctor_id):
    """
    Belirli bir doktora atanan tüm hastaları döner.
    """
    user = request.ctx.user  # Middleware tarafından sağlanan kullanıcı verisi
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    async with await get_db_connection() as conn:
        try:
            patients = await DoctorService.get_patients(conn, doctor_id)
            return response.json({"patients": patients}, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@doctor_bp.post("/<doctor_id>/availability")
@auth_middleware
async def set_availability(request, doctor_id):
    """
    Doktorun çalışma saatlerini belirler.
    """
    user = request.ctx.user
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    data = request.json
    required_fields = ["available_date", "available_start_time", "available_end_time"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await DoctorService.set_availability(
                conn,
                doctor_id,
                data["available_date"],
                data["available_start_time"],
                data["available_end_time"]
            )
            return response.json({"message": "Availability updated successfully", "data": result}, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@doctor_bp.post("/<doctor_id>/lab_tests")
@auth_middleware
async def request_lab_test(request, doctor_id):
    """
    Doktor için laboratuvar testi talebi oluşturur.
    """
    user = request.ctx.user
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    data = request.json
    required_fields = ["patient_id", "test_name", "priority"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    try:
        lab_test_data = {
            "doctor_id": doctor_id,
            "patient_id": data["patient_id"],
            "test_name": data["test_name"],
            "priority": data["priority"]
        }
        response = requests.post(f"{LAB_TEST_SERVICE_URL}/", json=lab_test_data)

        if response.status_code == 201:
            return response.json({"message": "Lab test requested successfully"}, status=201)
        else:
            return response.json({"error": "Failed to request lab test"}, status=500)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@doctor_bp.post("/<doctor_id>/prescriptions")
@auth_middleware
async def prescribe_medication(request, doctor_id):
    """
    Doktor reçete yazma endpoint'i.
    """
    user = request.ctx.user
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    data = request.json
    required_fields = ["patient_id", "medication_details"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await DoctorService.prescribe_medication(
                conn,
                doctor_id,
                data["patient_id"],
                data["medication_details"]
            )

            # Notification Service entegrasyonu
            notification_data = {
                "to_email": await DoctorService.get_patient_email(conn, data["patient_id"]),
                "subject": "New Prescription",
                "message": f"You have a new prescription from your doctor:\n\n{data['medication_details']}"
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service error: {e}")

            return response.json({"message": "Prescription added successfully", "data": result}, status=201)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@doctor_bp.put("/<doctor_id>/appointments/<appointment_id>")
@auth_middleware
async def modify_appointment(request, doctor_id, appointment_id):
    """
    Randevu düzenleme endpoint'i.
    """
    user = request.ctx.user
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    data = request.json
    required_fields = ["appointment_date", "appointment_time", "reason"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    async with await get_db_connection() as conn:
        try:
            result = await DoctorService.modify_appointment(
                conn,
                appointment_id,
                data["appointment_date"],
                data["appointment_time"],
                data["reason"]
            )

            # Notification Service entegrasyonu
            patient_email = await DoctorService.get_patient_email_by_appointment(conn, appointment_id)
            notification_data = {
                "to_email": patient_email,
                "subject": "Appointment Update",
                "message": f"Your appointment has been updated to:\n\nDate: {data['appointment_date']}\nTime: {data['appointment_time']}\nReason: {data['reason']}"
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service error: {e}")

            return response.json({"message": "Appointment updated successfully", "data": result}, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@doctor_bp.delete("/<doctor_id>/appointments/<appointment_id>")
@auth_middleware
async def cancel_appointment(request, doctor_id, appointment_id):
    """
    Doktorun bir randevuyu iptal etmesi için endpoint.
    """
    user = request.ctx.user
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    async with await get_db_connection() as conn:
        try:
            # Randevuyu iptal et
            await DoctorService.cancel_appointment(conn, appointment_id)

            # Notification Service entegrasyonu
            patient_email = await DoctorService.get_patient_email_by_appointment(conn, appointment_id)
            notification_data = {
                "to_email": patient_email,
                "subject": "Appointment Canceled",
                "message": "Your appointment has been canceled by your doctor. Please contact the hospital for further details."
            }
            try:
                requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
            except Exception as e:
                print(f"Notification Service error: {e}")

            return response.json({"message": "Appointment canceled successfully."}, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@doctor_bp.put("/<doctor_id>/patients/<patient_id>/notes")
@auth_middleware
async def manage_patient_notes(request, doctor_id, patient_id):
    """
    Doktorun hasta notlarını yönetmesi için endpoint.
    """
    user = request.ctx.user
    if user["role"] != "doctor" or user["id"] != int(doctor_id):
        return response.json({"error": "Unauthorized access"}, status=403)

    data = request.json
    notes = data.get("notes")

    if not notes:
        return response.json({"error": "Notes are required."}, status=400)

    async with await get_db_connection() as conn:
        try:
            await DoctorService.manage_patient_notes(conn, patient_id, notes)
            return response.json({"message": "Patient notes updated successfully."}, status=200)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)
