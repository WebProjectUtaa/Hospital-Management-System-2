from sanic import Blueprint, response
from app.services.notification_service import NotificationService
from app.db.init_db import get_db_connection

notification_bp = Blueprint("notifications", url_prefix="/notifications")

@notification_bp.route("/", methods=["POST"])
async def create_notification(request):
    """
    Yeni bir bildirim oluşturur.
    """
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

@notification_bp.route("/", methods=["GET"])
async def list_notifications(request):
    """
    Mevcut bildirim loglarını listeler.
    """
    conn = await get_db_connection()
    try:
        notifications = await NotificationService.list_notifications(conn)
        return response.json(notifications, status=200)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
    finally:
        await conn.ensure_closed()
