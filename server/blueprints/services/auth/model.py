from server.config.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:

    @staticmethod
    def create_user(name, email, password, is_admin=0):
        """
        Create a new user (User by default, admin if is_admin=1)
        """
        conn = get_connection()
        cur = conn.cursor()
        try:
            hashed = generate_password_hash(password)
            cur.execute("""
                INSERT INTO users (name, email, password_hash, is_admin)
                VALUES (%s, %s, %s, %s)
            """, (name, email, hashed, is_admin))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_user_by_email(email):
        """
        Fetch full user record by email
        """
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def user_exists(email):
        """
        Check if user exists
        """
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM users WHERE email=%s", (email,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_password(email, new_password):
        """
        Reset / update user password
        """
        conn = get_connection()
        cur = conn.cursor()
        try:
            hashed = generate_password_hash(new_password)
            cur.execute(
                "UPDATE users SET password_hash=%s WHERE email=%s",
                (hashed, email)
            )
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def verify_password(hashed_password, plain_password):
        """
        Verify plain password against hash
        """
        return check_password_hash(hashed_password, plain_password)
