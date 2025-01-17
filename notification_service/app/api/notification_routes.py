from sanic import Blueprint, response
from app.services.notification_service import NotificationService
from app.db.init_db import get_db_connection
from utils.auth_middleware import auth_middleware
from app.utils.email_sender import EmailSender


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

@notification_bp.post("/bulk")
@auth_middleware  # Add Auth Middleware
async def send_bulk_notifications(request):
    """
    Send notifications to multiple recipients.
    """
    user = request.ctx.user  # Middleware-provided user data
    if user["role"] != "admin":
        return response.json({"error": "Only admins can send bulk notifications."}, status=403)

    data = request.json
    notifications = data.get("notifications")  # List of notifications

    if not notifications or not isinstance(notifications, list):
        return response.json({"error": "Invalid or missing 'notifications' field."}, status=400)

    conn = await get_db_connection()
    try:
        results = []
        for notification in notifications:
            to_email = notification.get("to_email")
            subject = notification.get("subject")
            message = notification.get("message")

            if not to_email or not subject or not message:
                results.append({"error": f"Missing fields in notification: {notification}"})
                continue

            result = await NotificationService.create_notification(
                conn, to_email, subject, message
            )
            results.append(result)

        return response.json({"results": results}, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        await conn.ensure_closed()

@notification_bp.get("/health")
async def health_check(request):
    """
    Health check endpoint for Notification Service.
    """
    return response.json({"status": "Notification Service is running."}, status=200)

@notification_bp.get("/filter")
@auth_middleware  # Add Auth Middleware
async def filter_notifications(request):
    """
    Filter notification logs based on query parameters.
    """
    user = request.ctx.user  # Middleware-provided user data
    if user["role"] not in ["admin"]:
        return response.json({"error": "Unauthorized access."}, status=403)

    email = request.args.get("email")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    conn = await get_db_connection()
    try:
        notifications = await NotificationService.filter_notifications(conn, email, date_from, date_to)
        return response.json(notifications, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        await conn.ensure_closed()

@notification_bp.post("/send_email")
async def send_email(request):
    """
    Send an email notification.
    """
    data = request.json
    to_email = data.get("to_email")
    subject = data.get("subject")
    message = data.get("message")

    if not (to_email and subject and message):
        return response.json({"error": "Missing required fields."}, status=400)

    try:
        EmailSender.send_email(to_email, subject, message)
        return response.json({"message": "Email sent successfully"}, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)