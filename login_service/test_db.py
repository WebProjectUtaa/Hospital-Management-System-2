import asyncio
from app.db.init_db import init_db, get_db_connection, close_db

async def test_db_connection():
    # Veritabanı bağlantısını başlat
    await init_db()
    print("Database connection pool initialized.")

    # Bir bağlantı al ve test et
    conn = await get_db_connection()
    try:
        print("Database connection successful:", conn)

        # Basit bir test sorgusu çalıştır
        query = "SELECT 1 as test_value"
        async with conn.cursor() as cur:
            await cur.execute(query)
            result = await cur.fetchone()
            print("Test Query Result:", result)
    finally:
        # Bağlantıyı serbest bırak
        conn.close()

    # Bağlantı havuzunu kapat
    await close_db()
    print("Database connection pool closed.")

if __name__ == "__main__":
    asyncio.run(test_db_connection())
