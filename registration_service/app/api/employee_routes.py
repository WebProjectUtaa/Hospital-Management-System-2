from sanic import Blueprint, response
from app.services.employee_service import EmployeeService
from app.db.init_db import get_db_connection
from app.api.auth import role_required
import requests
import os
import logging

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8000/notifications")
APPOINTMENT_SERVICE_URL = os.getenv("APPOINTMENT_SERVICE_URL", "http://localhost:8001/appointments")

employee_bp = Blueprint("employee", url_prefix="/employees")

logger = logging.getLogger("employee_routes")

@employee_bp.post("/", name="add_employee")
@role_required(["admin"])
async def add_employee(request):
    """
    Add a new employee to the database and send a notification.
    """
    data = request.json
    required_fields = ["name", "surname", "role", "email", "gender"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return response.json({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)
    try:
        async with await get_db_connection() as conn:
            result = await EmployeeService.add_employee(conn, **data)
            
            # Notification Service Call
            notification_data = {
                "to_email": data["email"],
                "subject": "Welcome to Hospital Management System",
                "message": f"Dear {data['name']} {data['surname']},\n\nWelcome to our system as a {data['role']}. We are excited to have you on board!"
            }
            try:
                response = requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
                response.raise_for_status()
            except Exception as e:
                logger.error(f"Notification Service error: {e}")

            return response.json(result, status=201)
    except Exception as e:
        logger.error(f"Error adding employee: {e}")
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
        logger.error(f"Error retrieving employees: {e}")
        return response.json({"error": str(e)}, status=500)

@employee_bp.put("/<employee_id:int>", name="update_employee")
@role_required(["admin"])
async def update_employee(request, employee_id):
    """
    Update an existing employee's details and notify.
    """
    data = request.json
    if not data:
        return response.json({"error": "No data provided to update"}, status=400)
    try:
        async with await get_db_connection() as conn:
            result = await EmployeeService.update_employee(conn, employee_id, **data)

            # Notification Service Call
            notification_data = {
                "to_email": data.get("email"),
                "subject": "Your Profile Has Been Updated",
                "message": "Your employee profile details have been successfully updated."
            }
            try:
                response = requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
                response.raise_for_status()
            except Exception as e:
                logger.error(f"Notification Service error: {e}")

            return response.json(result, status=200)
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        return response.json({"error": str(e)}, status=500)

@employee_bp.delete("/<employee_id:int>", name="delete_employee")
@role_required(["admin"])
async def delete_employee(request, employee_id):
    """
    Delete an employee from the database and clean up related data.
    """
    try:
        async with await get_db_connection() as conn:
            # Fetch employee email before deletion for notification
            employee = await EmployeeService.get_employee_by_id(conn, employee_id)
            if not employee:
                return response.json({"error": "Employee not found"}, status=404)

            # Delete the employee
            result = await EmployeeService.delete_employee(conn, employee_id)

            # Notify the employee
            notification_data = {
                "to_email": employee["email"],
                "subject": "Account Deletion Notice",
                "message": "Your account has been removed from the system. If you have any questions, please contact the admin."
            }
            try:
                response = requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
                response.raise_for_status()
            except Exception as e:
                logger.error(f"Notification Service error: {e}")

            # Clean related appointments (if applicable)
            try:
                requests.delete(f"{APPOINTMENT_SERVICE_URL}/cleanup/{employee_id}")
            except Exception as e:
                logger.error(f"Appointment Service error: {e}")

            return response.json(result, status=200)
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        return response.json({"error": str(e)}, status=500)
