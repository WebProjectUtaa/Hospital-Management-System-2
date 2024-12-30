import aiohttp
from sanic import response
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")

def auth_middleware(handler):
    @wraps(handler)
    async def middleware(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return response.json({"error": "Missing Authorization header"}, status=401)
        
        token = token.replace("Bearer ", "")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{AUTH_SERVICE_URL}/auth/validate_token",
                    json={"token": token}
                ) as auth_response:
                    if auth_response.status == 200:
                        response_data = await auth_response.json()
                        request.ctx.user = response_data["data"]
                    else:
                        return response.json({"error": "Invalid token"}, status=401)
        except Exception as e:
            return response.json({"error": f"Failed to validate token: {e}"}, status=500)
        
        return await handler(request, *args, **kwargs)
    return middleware
