from sanic import Blueprint, response
from app.services.login_service import LoginService
from app.db.init_db import get_db_connection
from utils.jwt_utils import create_token, verify_token
from dotenv import load_dotenv
import os
import jwt
import requests

NOTIFICATION_SERVICE_URL = "http://localhost:8000/notifications"
APPOINTMENT_SERVICE_URL = "http://localhost:8001/appointments"

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# In-memory storage for invalidated tokens (replace with a DB if necessary)
revoked_tokens = set()

login_bp = Blueprint("login_routes", url_prefix="/login")

@login_bp.post("/")
async def login(request):
    """
    Kullanıcı login endpoint'i. Appointment Service ve Notification Service ile entegrasyon.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", None)

    if not email or not password:
        return response.json({"error": "Email and password are required"}, status=400)

    async with await get_db_connection() as conn:
        try:
            user = await LoginService.authenticate_user(conn, email, password, role)
            if user:
                access_token = create_token(
                    {"id": user["id"], "email": user["email"], "role": user["role"]},
                    SECRET_KEY,
                    expires_in=900
                )
                refresh_token = create_token(
                    {"id": user["id"]}, SECRET_KEY, expires_in=604800
                )

                # Fetch appointments if the user is a patient
                appointments = []
                if role == "patient":
                    try:
                        response = requests.get(
                            f"{APPOINTMENT_SERVICE_URL}/",
                            headers={"Authorization": f"Bearer {access_token}"}
                        )
                        if response.status_code == 200:
                            appointments = response.json()
                    except Exception as e:
                        print(f"Appointment Service error: {e}")

                # Send login notification
                notification_data = {
                    "to_email": email,
                    "subject": "Login Successful",
                    "message": f"Dear {user['role'].capitalize()},\n\nYou have successfully logged in.\n\nBest regards,\nHospital Management System"
                }
                try:
                    requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
                except Exception as e:
                    print(f"Notification Service error: {e}")

                return response.json({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "appointments": appointments
                }, status=200)
            else:
                return response.json({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return response.json({"error": str(e)}, status=500)

@login_bp.post("/refresh")
async def refresh_token(request):
    """
    Refresh token kullanarak yeni bir access token oluşturur.
    Notification Service ile entegrasyon.
    """
    data = request.json
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return response.json({"error": "Refresh token is missing"}, status=400)

    try:
        decoded_token = verify_token(refresh_token, SECRET_KEY)
        user_id = decoded_token["id"]

        # Yeni access token oluştur
        access_token = create_token(
            {"id": user_id}, SECRET_KEY, expires_in=900
        )

        # Send token refresh notification
        notification_data = {
            "to_email": decoded_token["email"],
            "subject": "Token Refreshed",
            "message": "Your token has been successfully refreshed."
        }
        try:
            requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return response.json({"access_token": access_token}, status=200)
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Refresh token expired"}, status=401)
    except jwt.InvalidTokenError:
        return response.json({"error": "Invalid token"}, status=401)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

@login_bp.post("/logout")
async def logout_user(request):
    """
    Kullanıcıyı logout yapar ve token'ı iptal eder.
    Notification Service ile entegrasyon.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return response.json({"error": "Unauthorized"}, status=401)

    token = auth_header.split(" ")[1]
    revoked_tokens.add(token)  # Token'ı revoked list'e ekle

    # Send logout notification
    try:
        notification_data = {
            "to_email": "user_email@example.com",  # Token'dan email almanız gerekebilir.
            "subject": "Logout Successful",
            "message": "You have successfully logged out."
        }
        requests.post(f"{NOTIFICATION_SERVICE_URL}/send_email", json=notification_data)
    except Exception as e:
        print(f"Notification Service error: {e}")

    return response.json({"message": "Logout successful. Redirect to login page."}, status=200)

@login_bp.post("/validate_token")
async def validate_token(request):
    """
    Validate JWT token.
    """
    token = request.json.get("token")
    if not token:
        return response.json({"error": "Token is missing"}, status=400)

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return response.json({"message": "Token is valid", "data": decoded}, status=200)
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return response.json({"error": "Invalid token"}, status=401)
