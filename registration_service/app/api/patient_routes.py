from sanic import Blueprint, response
from app.services.patient_service import PatientService
from app.services.patient_record_service import PatientRecordService
from app.db.init_db import get_db_connection

patient_bp = Blueprint("patients")

@patient_bp.post("/patients/register")
async def register_patient(request):
    data = request.json
    conn = await get_db_connection()

    try:
        result = await PatientService.add_patient(
            conn,
            data["name"], data["surname"], data["age"], data["blood_group"],
            data["gender"], data["contacts"], data["next_of_keen_contacts"],
            data["insurance"], data["email"], data["password"]
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

    try:
        result = await PatientService.update_patient(
            conn, patient_id,
            data.get("name"), data.get("surname"), data.get("contacts")
        )
        return response.json(result)
    finally:
        conn.close()

@patient_bp.delete("/patients/delete/<patient_id>")
async def delete_patient(request, patient_id):
    conn = await get_db_connection()

    try:
        result = await PatientService.delete_patient(conn, patient_id)
        return response.json(result)
    finally:
        conn.close()

@patient_bp.post("/records/register")
async def register_record(request):
    data = request.json
    conn = await get_db_connection()

    try:
        result = await PatientRecordService.add_record(
            conn,
            data["patient_id"], data["doctor_id"], data["department_id"],
            data["patient_status"], data["doctor_note"], data["prescription"]
        )
        return response.json(result)
    finally:
        conn.close()

@patient_bp.get("/records")
async def view_records(request):
    patient_id = request.args.get("patient_id")
    doctor_id = request.args.get("doctor_id")
    conn = await get_db_connection()

    try:
        records = await PatientRecordService.get_records(conn, patient_id, doctor_id)
        return response.json(records)
    finally:
        conn.close()

@patient_bp.put("/records/update/<record_id>")
async def update_record(request, record_id):
    data = request.json
    conn = await get_db_connection()

    try:
        result = await PatientRecordService.update_record(
            conn, record_id,
            data.get("patient_status"), data.get("doctor_note"), data.get("prescription")
        )
        return response.json(result)
    finally:
        conn.close()

@patient_bp.delete("/records/delete/<record_id>")
async def delete_record(request, record_id):
    conn = await get_db_connection()

    try:
        result = await PatientRecordService.delete_record(conn, record_id)
        return response.json(result)
    finally:
        conn.close()
