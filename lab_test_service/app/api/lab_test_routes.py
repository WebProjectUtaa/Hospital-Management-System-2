from sanic import Blueprint, response
from app.db.init_db import get_db_connection
from app.db.models import LabTest
from utils.auth_middleware import auth_middleware

lab_test_bp = Blueprint("lab_tests")

@lab_test_bp.post("/lab_tests")
@auth_middleware  # Add Auth Middleware
async def create_lab_test(request):
    """
    Create a new lab test.
    """
    user = request.ctx.user  # Middleware-provided user data
    if user["role"] != "doctor":
        return response.json({"error": "Only doctors can create lab tests."}, status=403)

    required_fields = ["patient_id", "doctor_id", "test_name", "priority"]
    for field in required_fields:
        if field not in request.json:
            return response.json({"error": f"Missing required field: {field}"}, status=400)

    patient_id = request.json["patient_id"]
    doctor_id = request.json["doctor_id"]
    test_name = request.json["test_name"]
    priority = request.json["priority"]

    async with get_db_connection() as conn:
        await LabTest.add(conn, patient_id, doctor_id, test_name, priority)
    return response.json({"message": "Lab test created successfully"}, status=201)

@lab_test_bp.get("/lab_tests")
@auth_middleware  # Add Auth Middleware
async def list_lab_tests(request):
    """
    List all lab tests for the authenticated user.
    """
    user = request.ctx.user  # Middleware-provided user data
    async with get_db_connection() as conn:
        if user["role"] == "doctor":
            tests = await LabTest.get_by_doctor(conn, user["id"])
        elif user["role"] == "patient":
            tests = await LabTest.get_by_patient(conn, user["id"])
        else:
            return response.json({"error": "Unauthorized"}, status=403)
    return response.json(tests, status=200)
