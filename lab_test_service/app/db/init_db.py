from aiomysql import DictCursor, create_pool

pool = None

async def init_db():
    global pool
    pool = await create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        db="register",
        cursorclass=DictCursor,
        autocommit=True
    )

async def get_db_connection():
    if pool is None:
        raise RuntimeError("Database connection is not initialized. Call 'init_db' first.")
    return await pool.acquire()

async def close_db():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
