from aiomysql import create_pool, DictCursor

pool = None

async def init_db():
    """
    Veritabanı bağlantısını başlatır.
    """
    global pool
    pool = await create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        db="hospital_management",
        cursorclass=DictCursor,
        autocommit=True
    )

async def get_db_connection():
    """
    Veritabanı bağlantısını alır.
    """
    if pool is None:
        raise RuntimeError("Database connection is not initialized. Call 'init_db' first.")
    return await pool.acquire()

async def close_db():
    """
    Veritabanı bağlantısını kapatır.
    """
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
