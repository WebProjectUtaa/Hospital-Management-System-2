from sanic import Blueprint, response
from app.services.doctor_service import DoctorService
from app.db.init_db import get_db_connection

doctor_bp = Blueprint("doctor")

@doctor_bp.post("/doctors/add")
async def add_doctor(request):
    data = request.json
    conn = await get_db_connection()
    try:
        result = await DoctorService.add_doctor(
            conn, data["name"], data["surname"], data["email"], 
            data["gender"], data["contacts"], data["degree"], 
            data["specialization"], data["password"]
        )
        return response.json(result)
    finally:
        conn.close()

@doctor_bp.get("/doctors")
async def get_all_doctors(request):
    conn = await get_db_connection()
    try:
        doctors = await DoctorService.get_all_doctors(conn)
        return response.json(doctors)
    finally:
        conn.close()
