from sanic import Blueprint, response
from app.services.patient_service import PatientService
from app.db.init_db import get_db_connection

patient_bp = Blueprint("patient")

@patient_bp.post("/patients/add")
async def add_patient(request):
    data = request.json
    conn = await get_db_connection()

    current_user_role = request.headers.get("Role")

    if current_user_role not in ["receptionist", "admin"]:
        return response.json({"error": "Unauthorized. Only receptionist or admin can add patients."}, status=403)

    try:
        result = await PatientService.add_patient(
            conn, data["name"], data["surname"], data["age"],
            data["blood_group"], data["gender"], data["contacts"],
            data["next_of_keen"], data["insurance"], data["email"],
            data["password"], current_user_role=current_user_role
        )
        return response.json(result)
    finally:
        conn.close()

@patient_bp.get("/patients")
async def get_all_patients(request):
    conn = await get_db_connection()
    try:
        patients = await PatientService.get_all_patients(conn)
        return response.json(patients)
    finally:
        conn.close()

@patient_bp.put("/patients/update/<patient_id>")
async def update_patient(request, patient_id):
    data = request.json
    conn = await get_db_connection()

    current_user_role = request.headers.get("Role")

    if current_user_role not in ["receptionist", "admin"]:
        return response.json({"error": "Unauthorized. Only receptionist or admin can update patients."}, status=403)

    try:
        result = await PatientService.update_patient(
            conn, patient_id, data.get("name"), data.get("surname"), data.get("contacts")
        )
        return response.json(result)
    finally:
        conn.close()

@patient_bp.delete("/patients/delete/<patient_id>")
async def delete_patient(request, patient_id):
    conn = await get_db_connection()

    current_user_role = request.headers.get("Role")

    if current_user_role != "admin":
        return response.json({"error": "Unauthorized. Only admins can delete patients."}, status=403)

    try:
        result = await PatientService.delete_patient(conn, patient_id)
        return response.json(result)
    finally:
        conn.close()
