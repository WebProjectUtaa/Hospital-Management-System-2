from aiomysql import create_pool, DictCursor

pool = None

async def init_db():
    """
    Veri tabanı bağlantı havuzunu başlatır.
    """
    global pool
    if pool is None:
        pool = await create_pool(
            host="localhost",
            port=3306,
            user="root",
            password="root",  # Kendi kullanıcı adı ve şifrenizi ekleyin
            db="registration",  # Notification Service için kullanılan veritabanı
            cursorclass=DictCursor,
            autocommit=True
        )
        print("Database connection pool initialized.")

async def get_db_connection():
    """
    Veri tabanından bir bağlantı alır.
    """
    global pool
    if pool is None:
        raise RuntimeError("Database connection pool is not initialized. Call 'init_db' first.")
    return await pool.acquire()

async def close_db():
    """
    Veri tabanı bağlantı havuzunu kapatır.
    """
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
        print("Database connection pool closed.")
