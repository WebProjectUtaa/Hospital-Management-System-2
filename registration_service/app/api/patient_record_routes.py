from sanic import Blueprint, response
from app.services.patient_record_service import PatientRecordService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware

record_bp = Blueprint("record", url_prefix="/records")

@record_bp.post("/")
@auth_middleware
async def add_record(request):
    """
    Add a new patient record.
    """
    user = request.ctx.user
    if user["role"] != "doctor":
        return response.json({"error": "Only doctors can add records."}, status=403)

    data = request.json
    required_fields = ["patient_id", "doctor_id", "department_id", "patient_status", "doctor_note"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        async with await get_db_connection() as conn:
            result = await PatientRecordService.add_record(conn, **data)
            return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@record_bp.get("/<patient_id:int>")
@auth_middleware
async def get_records_by_patient(request, patient_id):
    """
    Retrieve records by patient ID.
    """
    user = request.ctx.user
    if user["role"] not in ["doctor", "receptionist"]:
        return response.json({"error": "Only doctors or receptionists can view records."}, status=403)

    try:
        async with await get_db_connection() as conn:
            records = await PatientRecordService.get_records_by_patient(conn, patient_id)
            return response.json(records, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
