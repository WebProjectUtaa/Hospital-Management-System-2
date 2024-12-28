from sanic import Blueprint, response
from app.services.patient_record_service import PatientRecordService
from app.db.init_db import get_db_connection
import requests
import os

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8000/notifications")
APPOINTMENT_SERVICE_URL = os.getenv("APPOINTMENT_SERVICE_URL", "http://localhost:8001/appointments")

record_bp = Blueprint("record", url_prefix="/records")

@record_bp.post("/")
async def add_record(request):
    """
    Add a new patient record and notify.
    """
    data = request.json
    required_fields = ["patient_id", "doctor_id", "department_id", "patient_status", "doctor_note"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        conn = await get_db_connection()
        result = await PatientRecordService.add_record(conn, **data)

        # Notification Service Call
        notification_data = {
            "to_email": f"patient_{data['patient_id']}@example.com",
            "subject": "New Record Added",
            "message": "A new patient record has been added to your profile."
        }
        try:
            requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@record_bp.delete("/<record_id:int>")
async def delete_record(request, record_id):
    """
    Delete a patient record and related appointments.
    """
    try:
        conn = await get_db_connection()
        # Fetch record before deletion
        record = await PatientRecordService.get_by_id(conn, record_id)
        if not record:
            return response.json({"error": "Record not found"}, status=404)

        # Delete the record
        result = await PatientRecordService.delete_record(conn, record_id)

        # Notify the patient
        notification_data = {
            "to_email": f"patient_{record['patient_id']}@example.com",
            "subject": "Record Deleted",
            "message": "One of your records has been deleted from your profile."
        }
        try:
            requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
        except Exception as e:
            print(f"Notification Service error: {e}")

        # Clean related appointments (if applicable)
        try:
            requests.delete(f"{APPOINTMENT_SERVICE_URL}/cleanup/{record['patient_id']}")
        except Exception as e:
            print(f"Appointment Service error: {e}")

        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
