from sanic import Blueprint, response
from app.services.patient_service import PatientService
from app.db.init_db import get_db_connection
from app.api.auth import role_required

patient_bp = Blueprint("patient", url_prefix="/patients")

@patient_bp.post("/")
@role_required(["receptionist"]) 
async def add_patient(request):
    data = request.json
    required_fields = ["name", "surname", "age", "blood_group", "gender", "contacts", "keen_contacts", "insurance", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        conn = await get_db_connection()
        result = await PatientService.add_patient(conn, **data)
        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.get("/")
@role_required(["receptionist"])  # Receptionist hastaları görebilir
async def get_all_patients(request):
    try:
        conn = await get_db_connection()
        patients = await PatientService.get_all_patients(conn)
        return response.json(patients, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@patient_bp.put("/<patient_id:int>")
@role_required(["receptionist"])
async def update_patient(request, patient_id):
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update"}, status=400)
    try:
        conn = await get_db_connection()
        result = await PatientService.update_patient(conn, patient_id, data)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@patient_bp.delete("/<patient_id:int>")
@role_required(["receptionist"])  # Receptionist hasta silebilir
async def delete_patient(request, patient_id):
    try:
        conn = await get_db_connection()
        result = await PatientService.delete_patient(conn, patient_id)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
