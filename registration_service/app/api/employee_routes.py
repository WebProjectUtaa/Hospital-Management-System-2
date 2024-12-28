from sanic import Blueprint, response
from app.services.employee_service import EmployeeService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware

employee_bp = Blueprint("employee", url_prefix="/employees")

@employee_bp.post("/")
@auth_middleware
async def add_employee(request):
    """
    Add a new employee to the database.
    """
    user = request.ctx.user
    if user["role"] != "admin":
        return response.json({"error": "Only admins can add employees."}, status=403)

    data = request.json
    required_fields = ["name", "surname", "role", "email", "gender"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        async with await get_db_connection() as conn:
            result = await EmployeeService.add_employee(conn, **data)
            return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@employee_bp.get("/")
@auth_middleware
async def get_all_employees(request):
    """
    Retrieve all employees from the database.
    """
    user = request.ctx.user
    if user["role"] != "admin":
        return response.json({"error": "Only admins can view employees."}, status=403)

    try:
        async with await get_db_connection() as conn:
            employees = await EmployeeService.get_all_employees(conn)
            return response.json(employees, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
