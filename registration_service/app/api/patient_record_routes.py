from sanic import Blueprint, response
from app.services.patient_record_service import PatientRecordService
from app.db.init_db import get_db_connection

record_bp = Blueprint("patient_records")

@record_bp.post("/records/register")
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
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()

@record_bp.get("/records")
async def view_records(request):
    patient_id = request.args.get("patient_id")
    doctor_id = request.args.get("doctor_id")
    conn = await get_db_connection()

    try:
        records = await PatientRecordService.get_records(conn, patient_id, doctor_id)
        return response.json(records)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()

@record_bp.put("/records/update/<record_id>")
async def update_record(request, record_id):
    data = request.json
    conn = await get_db_connection()

    try:
        result = await PatientRecordService.update_record(
            conn, record_id,
            data.get("patient_status"), data.get("doctor_note"), data.get("prescription")
        )
        return response.json(result)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()

@record_bp.delete("/records/delete/<record_id>")
async def delete_record(request, record_id):
    conn = await get_db_connection()

    try:
        result = await PatientRecordService.delete_record(conn, record_id)
        return response.json(result)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()
