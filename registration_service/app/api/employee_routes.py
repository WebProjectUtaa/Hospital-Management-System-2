from sanic import Blueprint, response
from app.services.employee_service import EmployeeService
from app.db.init_db import get_db_connection
from app.api.auth import role_required

employee_bp = Blueprint("employee", url_prefix="/employees")

@employee_bp.post("/")
@role_required(["admin"]) 
async def add_employee(request):
    data = request.json
    required_fields = ["name", "surname", "role", "email", "gender"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        conn = await get_db_connection()
        result = await EmployeeService.add_employee(conn, **data)
        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@employee_bp.get("/")
@role_required(["admin"])  
async def get_all_employees(request):
    try:
        conn = await get_db_connection()
        employees = await EmployeeService.get_all_employees(conn)
        return response.json(employees, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@employee_bp.put("/<employee_id:int>")
@role_required(["admin"])
async def update_employee(request, employee_id):
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update"}, status=400)
    try:
        conn = await get_db_connection()
        result = await EmployeeService.update_employee(conn, employee_id, **data)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@employee_bp.delete("/<employee_id:int>")
@role_required(["admin"])
async def delete_employee(request, employee_id):
    try:
        conn = await get_db_connection()
        result = await EmployeeService.delete_employee(conn, employee_id)
        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
