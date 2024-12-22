from sanic import Blueprint, response
from app.services.patient_record_service import PatientRecordService
from app.db.init_db import get_db_connection

record_bp = Blueprint("record", url_prefix="/records")

@record_bp.post("/")
async def add_record(request):
    data = request.json
    required_fields = ["patient_id", "doctor_id", "department_id", "patient_status", "doctor_note"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        conn = await get_db_connection()
        result = await PatientRecordService.add_record(conn, **data)
        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@record_bp.get("/<patient_id:int>")
async def get_records_by_patient(request, patient_id):
    try:
        conn = await get_db_connection()
        records = await PatientRecordService.get_records_by_patient(conn, patient_id)
        return response.json(records, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@record_bp.put("/<record_id:int>")
async def update_record(request, record_id):
    data = request.json
    if not data:
        return response.json({"error": "No data provided"}, status=400)
    try:
        conn = await get_db_connection()
        result = await PatientRecordService.update_record(conn, record_id, data)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@record_bp.delete("/<record_id:int>")
async def delete_record(request, record_id):
    try:
        conn = await get_db_connection()
        result = await PatientRecordService.delete_record(conn, record_id)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
