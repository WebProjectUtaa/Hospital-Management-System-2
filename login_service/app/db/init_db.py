from aiomysql import create_pool, DictCursor

pool = None  # Global connection pool

async def init_db():
    """
    Initialize the database connection pool.
    """
    global pool
    if pool is None:
        pool = await create_pool(
            host="localhost",
            port=3306,
            user="root",
            password="root",  # Veritabanı şifrenizi buraya yazın
            db="registration",  # Kullanılan veritabanı ismi
            cursorclass=DictCursor,
            autocommit=True
        )

async def get_db_connection():
    """
    Get a connection from the pool.
    """
    global pool
    if pool is None:
        raise RuntimeError("Database connection pool is not initialized. Call 'init_db' first.")
    return await pool.acquire()

async def close_db():
    """
    Close the database connection pool.
    """
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
