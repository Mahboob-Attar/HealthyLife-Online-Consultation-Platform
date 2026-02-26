import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

# ---- Detect Railway vs Local ----
DB_CONFIG = {
    "host": os.getenv("MYSQLHOST") or os.getenv("DB_HOST"),
    "user": os.getenv("MYSQLUSER") or os.getenv("DB_USER"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASS"),
    "database": os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME"),
    "port": int(os.getenv("MYSQLPORT", 3306)),
    "auth_plugin": "caching_sha2_password",
    "connection_timeout": 5
}

# ---- Shared Connection Pool ----
connection_pool = pooling.MySQLConnectionPool(
    pool_name="main_pool",
    pool_size=int(os.getenv("DB_POOL_SIZE", 10)),  # reduce for free tier
    pool_reset_session=True,
    **DB_CONFIG
)

def get_connection():
    return connection_pool.get_connection()