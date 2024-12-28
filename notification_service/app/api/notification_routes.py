from sanic import Blueprint, response
from app.services.notification_service import NotificationService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware

notification_bp = Blueprint("notifications", url_prefix="/notifications")

@notification_bp.post("/")
@auth_middleware  # Add Auth Middleware
async def create_notification(request):
    """
    Create a new notification.
    """
    user = request.ctx.user  # Middleware-provided user data
    if user["role"] != "admin":
        return response.json({"error": "Only admins can send notifications."}, status=403)

    data = request.json
    to_email = data.get("to_email")
    subject = data.get("subject")
    message = data.get("message")

    if not to_email or not subject or not message:
        return response.json({"error": "Missing required fields."}, status=400)

    conn = await get_db_connection()
    try:
        result = await NotificationService.create_notification(
            conn, to_email, subject, message
        )
        return response.json(result, status=201)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        await conn.ensure_closed()

@notification_bp.get("/")
@auth_middleware  # Add Auth Middleware
async def list_notifications(request):
    """
    List notification logs.
    """
    user = request.ctx.user  # Middleware-provided user data
    if user["role"] not in ["admin", "doctor"]:
        return response.json({"error": "Unauthorized access."}, status=403)

    conn = await get_db_connection()
    try:
        notifications = await NotificationService.list_notifications(conn)
        return response.json(notifications, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        await conn.ensure_closed()
