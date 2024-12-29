from aiomysql import create_pool, DictCursor

_pool = None

async def init_db():
    """
    Veritabanı bağlantı havuzunu başlatır.
    """
    global _pool
    if _pool is None:
        _pool = await create_pool(
            host="localhost",
            port=3306,
            user="root",
            password="root", 
            db="registration",
            cursorclass=DictCursor,
            autocommit=True
        )
        print("Database connection pool initialized.")

async def get_db_connection():
    """
    Veritabanı bağlantısını alır.
    """
    global _pool
    if not _pool:
        raise RuntimeError("Database connection pool is not initialized. Call `init_db` first.")
    conn = await _pool.acquire()
    return conn

async def close_db():
    """
    Veritabanı bağlantı havuzunu kapatır.
    """
    global _pool
    if _pool:
        _pool.close()
        await _pool.wait_closed()
        print("Database connection pool closed.")
