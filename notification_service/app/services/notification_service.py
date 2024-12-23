from app.utils.email_sender import EmailSender
from app.db.models import NotificationLog

class NotificationService:
    @staticmethod
    async def create_notification(conn, to_email, subject, message):
        """
        Yeni bir bildirim oluşturur ve e-posta gönderir.
        """
        try:
            # E-posta gönder
            EmailSender.send_email(to_email, subject, message)

            # Başarıyla gönderilen bildirimi logla
            await NotificationLog.log_notification(conn, to_email, subject, message, "sent")
            return {"message": f"Notification successfully sent to {to_email}"}
        except Exception as e:
            # Hata durumunda logla
            await NotificationLog.log_notification(conn, to_email, subject, message, "failed")
            raise RuntimeError(f"Failed to create notification for {to_email}: {e}")

    @staticmethod
    async def list_notifications(conn):
        """
        Veritabanından tüm bildirimleri listeler.
        """
        return await NotificationLog.list_all(conn)
