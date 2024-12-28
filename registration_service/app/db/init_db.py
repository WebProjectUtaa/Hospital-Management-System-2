from aiomysql import create_pool

_pool = None

async def init_db():
    global _pool
    _pool = await create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        db="registration",
        autocommit=True
    )

async def get_db_connection():
    if not _pool:
        raise RuntimeError("Database connection pool is not initialized")
    conn = await _pool.acquire()
    return conn

async def close_db():
    if _pool:
        _pool.close()
        await _pool.wait_closed()
