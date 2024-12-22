from aiomysql import create_pool, DictCursor

pool = None

async def init_db():
    global pool
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
    if pool is None:
        raise RuntimeError("Veritabanına bağlanılamadı. 'init_db' çağrılmamış olabilir.")
    return await pool.acquire()

async def close_db():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        pool = None
