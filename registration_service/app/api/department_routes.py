from sanic import Blueprint, response
from app.services.department_service import DepartmentService
from app.db.init_db import get_db_connection
import requests
import os

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8000/notifications")

department_bp = Blueprint("department", url_prefix="/departments")

@department_bp.post("/")
async def add_department(request):
    """
    Add a new department and notify employees.
    """
    data = request.json
    required_fields = ["department_id", "department_name", "employee_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        conn = await get_db_connection()
        result = await DepartmentService.add_department(conn, **data)

        # Notify the employee
        notification_data = {
            "to_email": f"employee_{data['employee_id']}@example.com",
            "subject": "Department Assignment",
            "message": f"You have been assigned to the department: {data['department_name']}."
        }
        try:
            requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@department_bp.delete("/<department_id:int>")
async def delete_department(request, department_id):
    """
    Delete a department and notify employees.
    """
    try:
        conn = await get_db_connection()
        # Fetch department before deletion
        department = await DepartmentService.get_by_id(conn, department_id)
        if not department:
            return response.json({"error": "Department not found"}, status=404)

        # Delete the department
        result = await DepartmentService.delete_department(conn, department_id)

        # Notify employees in the department
        notification_data = {
            "to_email": f"all@department_{department_id}.example.com",
            "subject": "Department Closure",
            "message": f"The department {department['department_name']} has been closed."
        }
        try:
            requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return response.json(result, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
