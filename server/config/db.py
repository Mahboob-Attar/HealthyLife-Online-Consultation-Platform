import os
from mysql.connector import pooling
from dotenv import load_dotenv

# Load .env variables into environment
load_dotenv()

# ---- Database Config ----
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "auth_plugin": "caching_sha2_password",
    "connection_timeout": 5
}
# ---- Shared Connection Pool ----
connection_pool = pooling.MySQLConnectionPool(
    pool_name="main_pool",
    pool_size=int(os.getenv("DB_POOL_SIZE", 40)),
    pool_reset_session=True,
    **DB_CONFIG
)

def get_connection():
    """Return a pooled DB connection"""
    return connection_pool.get_connection()
