from aiomysql import create_pool, DictCursor

pool = None

async def init_db():
    """
    Veritabanı bağlantı havuzunu başlatır.
    """
    global pool
    if pool is None:
        pool = await create_pool(
            host="localhost",
            port=3306,
            user="root",
            password="root",  # Şifreyi kendi veritabanı ayarlarınıza göre değiştirin
            db="registration",  # Kullanılan veritabanının adı
            cursorclass=DictCursor,
            autocommit=True
        )

async def get_db_connection():
    """
    Veritabanı bağlantısı alır.
    """
    global pool
    if pool is None:
        raise RuntimeError("Database connection pool is not initialized. Call 'init_db' first.")
    return await pool.acquire()

async def close_db():
    """
    Veritabanı bağlantı havuzunu kapatır.
    """
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
