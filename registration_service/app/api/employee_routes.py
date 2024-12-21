from sanic import Blueprint, response
from app.services.employee_service import EmployeeService
from app.db.init_db import get_db_connection

employee_bp = Blueprint("employee")

@employee_bp.post("/employees/add")
async def add_employee(request):
    data = request.json
    conn = await get_db_connection()

    current_user_role = request.headers.get("Role")

    if current_user_role != "admin":
        return response.json({"error": "Unauthorized. Only admins can add employees."}, status=403)

    try:
        result = await EmployeeService.add_employee(
            conn, data["name"], data["surname"], data["role"],
            data["email"], data["gender"], data.get("contacts"),
            data.get("department"), current_user_role=current_user_role
        )
        return response.json(result)
    finally:
        conn.close()

@employee_bp.get("/employees")
async def get_all_employees(request):
    conn = await get_db_connection()
    try:
        employees = await EmployeeService.get_all_employees(conn)
        return response.json(employees)
    finally:
        conn.close()

@employee_bp.put("/employees/update/<employee_id>")
async def update_employee(request, employee_id):
    data = request.json
    conn = await get_db_connection()

    current_user_role = request.headers.get("Role")

    if current_user_role != "admin":
        return response.json({"error": "Unauthorized. Only admins can update employees."}, status=403)

    try:
        result = await EmployeeService.update_employee(
            conn, employee_id, data.get("name"), data.get("surname"), data.get("contacts")
        )
        return response.json(result)
    finally:
        conn.close()

@employee_bp.delete("/employees/delete/<employee_id>")
async def delete_employee(request, employee_id):
    conn = await get_db_connection()

    current_user_role = request.headers.get("Role")

    if current_user_role != "admin":
        return response.json({"error": "Unauthorized. Only admins can delete employees."}, status=403)

    try:
        result = await EmployeeService.delete_employee(conn, employee_id)
        return response.json(result)
    finally:
        conn.close()
