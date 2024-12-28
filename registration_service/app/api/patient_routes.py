from sanic import Blueprint, response
from app.services.patient_service import PatientService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware

patient_bp = Blueprint("patient", url_prefix="/patients")

@patient_bp.post("/")
@auth_middleware
async def add_patient(request):
    """
    Add a new patient.
    """
    user = request.ctx.user
    if user["role"] != "receptionist":
        return response.json({"error": "Only receptionists can add patients."}, status=403)

    data = request.json
    required_fields = ["name", "surname", "age", "blood_group", "gender", "contacts", "keen_contacts", "insurance", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

    try:
        async with await get_db_connection() as conn:
            result = await PatientService.add_patient(conn, **data)
            return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.get("/")
@auth_middleware
async def get_all_patients(request):
    """
    Retrieve all patients.
    """
    user = request.ctx.user
    if user["role"] != "receptionist":
        return response.json({"error": "Only receptionists can view patients."}, status=403)

    try:
        async with await get_db_connection() as conn:
            patients = await PatientService.get_all_patients(conn)
            return response.json(patients, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
