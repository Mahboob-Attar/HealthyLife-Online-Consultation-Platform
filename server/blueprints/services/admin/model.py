from server.config.db import get_connection

class AdminModel:

    @staticmethod
    def count_doctors():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) AS total FROM doctors")
        total = cur.fetchone()["total"]
        cur.close(); conn.close()
        return total

    @staticmethod
    def count_doctors_by_specialization():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT specialization, COUNT(*) AS count FROM doctors GROUP BY specialization")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows

    @staticmethod
    def get_feedback_ratings():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        ratings = {str(i): 0 for i in range(1, 6)}
        cur.execute("SELECT rating, COUNT(*) AS count FROM feedback GROUP BY rating")

        for row in cur.fetchall():
            ratings[str(row["rating"])] = row["count"]

        cur.close(); conn.close()
        return {"feedback_ratings": ratings}

    @staticmethod
    def get_feedback_list():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
