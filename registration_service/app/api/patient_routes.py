from sanic import Blueprint, response
from app.services.patient_service import PatientService
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
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()

@patient_bp.get("/patients")
async def get_patients(request):
    conn = await get_db_connection()

    try:
        patients = await PatientService.get_all_patients(conn)
        return response.json(patients)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
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
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()

@patient_bp.delete("/patients/delete/<patient_id>")
async def delete_patient(request, patient_id):
    conn = await get_db_connection()

    try:
        result = await PatientService.delete_patient(conn, patient_id)
        return response.json(result)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        conn.close()
