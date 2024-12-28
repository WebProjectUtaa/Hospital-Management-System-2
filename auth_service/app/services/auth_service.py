from utils.jwt_utils import create_token
from utils.http_utils import make_get_request, make_post_request

class AuthService:
    @staticmethod
    async def authenticate_employee(email, password):
        """
        Employees tablosunda kimlik doğrulama (Login Service ile iletişim).
        """
        url = f"http://localhost:8002/login"
        data = {"email": email, "password": password, "role": "employee"}
        response = make_post_request(url, data)
        if response and response.get("token"):
            return response
        raise ValueError("Invalid credentials for employee")

    @staticmethod
    async def authenticate_patient(email, password):
        """
        Patients tablosunda kimlik doğrulama (Login Service ile iletişim).
        """
        url = f"http://localhost:8002/login"
        data = {"email": email, "password": password, "role": "patient"}
        response = make_post_request(url, data)
        if response and response.get("token"):
            return response
        raise ValueError("Invalid credentials for patient")

    @staticmethod
    def authorize_token(token):
        """
        Token doğrulama ve kullanıcı bilgisi döndürme.
        """
        payload = make_post_request("http://localhost:8002/refresh", {"refresh_token": token})
        if payload:
            return payload
        raise ValueError("Invalid or expired token")
