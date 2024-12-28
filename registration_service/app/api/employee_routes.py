from sanic import Blueprint, response
from app.services.employee_service import EmployeeService
from app.db.init_db import get_db_connection
from app.api.auth import role_required

employee_bp = Blueprint("employee", url_prefix="/employees")

@employee_bp.post("/", name="add_employee")
@role_required(["admin"])
async def add_employee(request):
    """
    Add a new employee to the database.
    """
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

@employee_bp.get("/", name="get_all_employees")
@role_required(["admin"])
async def get_all_employees(request):
    """
    Retrieve all employees from the database.
    """
    try:
        async with await get_db_connection() as conn:
            employees = await EmployeeService.get_all_employees(conn)
            return response.json(employees, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@employee_bp.put("/<employee_id:int>", name="update_employee")
@role_required(["admin"])
async def update_employee(request, employee_id):
    """
    Update an existing employee's details.
    """
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update"}, status=400)
    try:
        async with await get_db_connection() as conn:
            result = await EmployeeService.update_employee(conn, employee_id, **data)
            return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@employee_bp.delete("/<employee_id:int>", name="delete_employee")
@role_required(["admin"])
async def delete_employee(request, employee_id):
    """
    Delete an employee from the database.
    """
    try:
        async with await get_db_connection() as conn:
            result = await EmployeeService.delete_employee(conn, employee_id)
            return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
