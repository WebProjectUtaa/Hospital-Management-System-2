from sanic import Blueprint, response
from app.services.appointment_service import AppointmentService
from app.db.init_db import get_db_connection
from app.api.auth_middleware import role_required

appointment_bp = Blueprint("appointment", url_prefix="/appointments")

@appointment_bp.post("/")
@role_required(["patient"])  # Sadece hastalar randevu oluşturabilir
async def create_appointment(request):
    data = request.json
    required_fields = ["patient_id", "doctor_id", "appointment_date", "appointment_time", "reason"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

    try:
        conn = await get_db_connection()
        result = await AppointmentService.create_appointment(conn, **data)
        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@appointment_bp.get("/")
@role_required(["doctor", "patient"])  # Hastalar kendi randevularını, doktorlar ise hastalarının randevularını görebilir
async def get_appointments(request):
    user = request.ctx.user
    try:
        conn = await get_db_connection()
        if user["role"] == "patient":
            appointments = await AppointmentService.get_appointments_by_patient(conn, user["id"])
        elif user["role"] == "doctor":
            appointments = await AppointmentService.get_appointments_by_doctor(conn, user["id"])
        else:
            return response.json({"error": "Unauthorized"}, status=403)

        return response.json(appointments, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@appointment_bp.put("/<appointment_id:int>")
@role_required(["doctor"])  # Sadece doktorlar randevuları güncelleyebilir
async def update_appointment(request, appointment_id):
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update"}, status=400)

    try:
        conn = await get_db_connection()
        result = await AppointmentService.update_appointment(conn, appointment_id, data)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@appointment_bp.delete("/<appointment_id:int>")
@role_required(["doctor", "patient"])  # Hastalar ve doktorlar randevuları iptal edebilir
async def delete_appointment(request, appointment_id):
    user = request.ctx.user
    try:
        conn = await get_db_connection()
        if user["role"] == "doctor":
            result = await AppointmentService.delete_appointment_by_doctor(conn, appointment_id, user["id"])
        elif user["role"] == "patient":
            result = await AppointmentService.delete_appointment_by_patient(conn, appointment_id, user["id"])
        else:
            return response.json({"error": "Unauthorized"}, status=403)

        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
