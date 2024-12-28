from utils.jwt_utils import create_token
from app.utils.hash_utils import HashUtils  # Import the HashUtils class
from app.db.models import AuthModel

class AuthService:
    @staticmethod
    async def authenticate_employee(conn, email, password):
        """
        Employees tablosunda kimlik doğrulama.
        """
        employee = await AuthModel.get_employee_by_email(conn, email)
        if not employee or not HashUtils.verify_password(password, employee["password"]):
            return {"error": "Invalid credentials"}

        # JWT token oluştur
        token = create_token({
            "id": employee["id"],
            "email": employee["email"],
            "role": employee["role"]
        })
        return {"message": "Login successful", "token": token}

    @staticmethod
    async def authenticate_patient(conn, email, password):
        """
        Patients tablosunda kimlik doğrulama.
        """
        patient = await AuthModel.get_patient_by_email(conn, email)
        if not patient or not HashUtils.verify_password(password, patient["password"]):
            return {"error": "Invalid credentials"}

        # JWT token oluştur
        token = create_token({
            "id": patient["id"],
            "email": patient["email"],
            "role": "patient"
        })
        return {"message": "Login successful", "token": token}
