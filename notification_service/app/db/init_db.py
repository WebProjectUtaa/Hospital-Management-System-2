from aiomysql import create_pool, DictCursor
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_NAME = os.getenv("DB_NAME", "registration")

pool = None  # Global connection pool

async def init_db():
    """
    Initialize the database connection pool.
    """
    global pool
    if pool is None:
        pool = await create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
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
