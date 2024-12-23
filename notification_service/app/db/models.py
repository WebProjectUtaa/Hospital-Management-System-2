class NotificationLog:
    @staticmethod
    async def log_notification(conn, to_email, subject, message, status):
        """
        Bildirim loglarını veritabanına kaydeder.
        """
        query = """
        INSERT INTO notification_log (to_email, subject, message, status)
        VALUES (%s, %s, %s, %s)
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (to_email, subject, message, status))
            await conn.commit()

    @staticmethod
    async def list_all(conn):
        """
        Tüm bildirimleri loglardan getirir.
        """
        query = "SELECT * FROM notification_log ORDER BY sent_at DESC"
        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()
