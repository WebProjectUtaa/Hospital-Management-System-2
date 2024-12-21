from sanic import Blueprint, response
from app.services.nurse_service import NurseService
from app.db.init_db import get_db_connection

nurse_bp = Blueprint("nurse")

@nurse_bp.post("/nurses/add")
async def add_nurse(request):
    data = request.json
    conn = await get_db_connection()
    try:
        result = await NurseService.add_nurse(
            conn, data["name"], data["surname"], data["email"], 
            data["gender"], data["contacts"], data["degree"], 
            data["password"]
        )
        return response.json(result)
    finally:
        conn.close()

@nurse_bp.get("/nurses")
async def get_all_nurses(request):
    conn = await get_db_connection()
    try:
        nurses = await NurseService.get_all_nurses(conn)
        return response.json(nurses)
    finally:
        conn.close()
