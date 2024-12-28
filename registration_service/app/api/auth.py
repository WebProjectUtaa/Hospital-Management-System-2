from utils.jwt_utils import verify_token
from sanic import response
from dotenv import load_dotenv
import os

# Çevresel değişkenleri yükle
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def role_required(allowed_roles):
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return response.json({"error": "Authorization token is missing"}, status=403)
            try:
                # Bearer ön ekini kaldır
                token = token.split("Bearer ")[-1]
                # Tokeni doğrula
                decoded_token = verify_token(token, SECRET_KEY)
                user_role = decoded_token.get("role")
                if user_role not in allowed_roles:
                    return response.json({"error": f"Access denied for role: {user_role}"}, status=403)
            except Exception as e:
                return response.json({"error": str(e)}, status=403)
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
