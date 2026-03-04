from server.config.db import get_connection

class FeedbackModel:

    @staticmethod
    def create(user_id: int, rating: int, review: str):
        conn = get_connection()
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO feedback (user_id, rating, review)
                VALUES (%s, %s, %s)
            """
            cur.execute(sql, (user_id, rating, review))
            conn.commit()
            return True
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT f.id, u.name, f.rating, f.review, f.created_at
                FROM feedback f
                JOIN users u ON f.user_id = u.id
                ORDER BY f.created_at DESC
            """)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
