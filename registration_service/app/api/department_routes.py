from sanic import Blueprint, response
from app.services.department_service import DepartmentService
from app.db.init_db import get_db_connection

department_bp = Blueprint("department", url_prefix="/departments")

@department_bp.post("/")
async def add_department(request):
    data = request.json
    required_fields = ["department_id", "department_name", "employee_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        conn = await get_db_connection()
        result = await DepartmentService.add_department(conn, **data)
        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@department_bp.get("/")
async def get_all_departments(request):
    try:
        conn = await get_db_connection()
        departments = await DepartmentService.get_all_departments(conn)
        return response.json(departments, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
