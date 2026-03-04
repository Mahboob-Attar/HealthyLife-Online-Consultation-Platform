import os
from config.db import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Path to init.sql
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sql_path = os.path.join(base_dir, "mysql-init", "init.sql")

    with open(sql_path, "r") as f:
        sql_script = f.read()

    for statement in sql_script.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()