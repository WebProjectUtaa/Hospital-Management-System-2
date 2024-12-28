from sanic import Blueprint, response
from app.db.init_db import get_db_connection
from app.db.models import LabTest

lab_test_bp = Blueprint("lab_tests")

@lab_test_bp.post("/lab_tests")
async def create_lab_test(request):
    """Create a new lab test"""
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
async def list_lab_tests(request):
    """List all lab tests"""
    async with get_db_connection() as conn:
        tests = await LabTest.get_all(conn)
    return response.json(tests, status=200)

@lab_test_bp.put("/lab_tests/<test_id:int>")
async def update_lab_test_status(request, test_id):
    """Update the status and result of a lab test"""
    if "status" not in request.json:
        return response.json({"error": "Missing required field: status"}, status=400)

    status = request.json["status"]
    result = request.json.get("result")

    async with get_db_connection() as conn:
        await LabTest.update_status(conn, test_id, status, result)
    return response.json({"message": "Lab test updated successfully"}, status=200)

@lab_test_bp.delete("/lab_tests/<test_id:int>")
async def delete_lab_test(request, test_id):
    """Delete a lab test"""
    async with get_db_connection() as conn:
        await LabTest.delete(conn, test_id)
    return response.json({"message": "Lab test deleted successfully"}, status=204)