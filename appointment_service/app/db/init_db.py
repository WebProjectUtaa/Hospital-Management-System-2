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
            password="root",
            db="registration",
            cursorclass=DictCursor,
            autocommit=True
        )


async def get_db_connection():
    global pool
    if pool is None:
        raise RuntimeError("Database connection pool is not initialized. Call 'init_db' first.")
    return pool



async def close_db():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
