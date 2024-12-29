from sanic import Blueprint, response
from app.services.appointment_service import AppointmentService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware

appointment_bp = Blueprint("appointment", url_prefix="/appointments")

@appointment_bp.get("/")
@auth_middleware
async def get_appointments(request):
    """
    Fetch appointments for the authenticated user.
    """
    user = request.ctx.user
    try:
        async with get_db_connection() as conn:
            if user["role"] == "patient":
                appointments = await AppointmentService.get_appointments_by_patient(conn, user["id"])
            elif user["role"] == "doctor":
                appointments = await AppointmentService.get_appointments_by_doctor(conn, user["id"])
            else:
                return response.json({"error": "Unauthorized"}, status=403)

            return response.json(appointments, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@appointment_bp.post("/")
@auth_middleware
async def create_appointment(request):
    """
    Create a new appointment for the authenticated patient.
    """
    user = request.ctx.user
    if user["role"] != "patient":
        return response.json({"error": "Only patients can create appointments."}, status=403)

    data = request.json
    required_fields = ["patient_id", "doctor_id", "appointment_date", "appointment_time", "reason"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

    try:
        async with get_db_connection() as conn:
            result = await AppointmentService.create_appointment(conn, **data)
            return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
