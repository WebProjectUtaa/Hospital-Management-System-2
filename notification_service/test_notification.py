import asyncio
from app.db.init_db import init_db, get_db_connection
from app.services.notification_service import NotificationService

async def test_notification_service():
    await init_db()
    conn = await get_db_connection()

    try:
        # Bildirim Oluşturma
        print("Testing Notification Creation...")
        creation_result = await NotificationService.create_notification(
            conn,
            to_email="webprojectutaa@gmail.com",
            subject="Test Notification",
            message="This is a test notification from the Notification Service."
        )
        print("Notification Creation Result:", creation_result)

        # Bildirimleri Listeleme
        print("Testing Notification Listing...")
        notifications = await NotificationService.list_notifications(conn)
        print("Notifications:", notifications)

    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        if conn:
            await conn.ensure_closed()

if __name__ == "__main__":
    asyncio.run(test_notification_service())
