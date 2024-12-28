from sanic import Blueprint, response
from app.services.login_service import LoginService
from app.db.init_db import get_db_connection
from utils.jwt_utils import create_token
from dotenv import load_dotenv
import os
import jwt

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# In-memory storage for invalidated tokens (replace with a DB if necessary)
revoked_tokens = set()

login_bp = Blueprint("login_routes", url_prefix="/login")

@login_bp.post("/")
async def login(request):
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
                access_token = create_token({"id": user["id"], "email": user["email"], "role": user["role"]}, SECRET_KEY, expires_in=9000)
                refresh_token = create_token({"id": user["id"]}, SECRET_KEY, expires_in=604800)
                return response.json({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, status=200)
            else:
                return response.json({"error": "Invalid credentials"}, status=401)
        except ConnectionError:
            return response.json({"error": "Database connection failed"}, status=500)
        except Exception as e:
            return response.json({"error": f"Unexpected error: {str(e)}"}, status=500)

@login_bp.post("/refresh")
async def refresh_token(request):
    data = request.json
    refresh_token = data.get("refresh_token")

    try:
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token["id"]
        if refresh_token in revoked_tokens:
            return response.json({"error": "Token has been revoked"}, status=401)
        access_token = create_token({"id": user_id}, SECRET_KEY, expires_in=9000)
        return response.json({"access_token": access_token}, status=200)
    except jwt.ExpiredSignatureError:
        return response.json({"error": "Refresh token expired"}, status=401)
    except jwt.InvalidTokenError:
        return response.json({"error": "Invalid token"}, status=401)
    except Exception as e:
        return response.json({"error": f"Unexpected error: {str(e)}"}, status=500)

@login_bp.post("/logout")
async def logout_user(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return response.json({"error": "Unauthorized"}, status=401)
    
    token = auth_header.split(" ")[1]
    revoked_tokens.add(token)  # Add the token to the revoked list
    return response.json({"message": "Logout successful. Redirect to login page."}, status=200)