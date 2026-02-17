from server.config.db import get_connection


class DashboardModel:

    # ================= TOTAL DOCTORS =================
    @staticmethod
    def get_total_doctors():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT COUNT(*) AS total FROM doctors WHERE status='approved'")
        result = cur.fetchone()

        cur.close()
        conn.close()

        return result["total"] if result else 0


    # ================= SPECIALIZATION COUNTS =================
    @staticmethod
    def get_specializations():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT specialization, COUNT(*) AS count
            FROM doctors
            WHERE status='approved'
            GROUP BY specialization
        """)

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results


    # ================= FEEDBACK RATINGS =================
    @staticmethod
    def get_feedback_ratings():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT rating, COUNT(*) AS count
            FROM feedback
            GROUP BY rating
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        ratings = {str(i): 0 for i in range(1, 6)}
        for r in rows:
            ratings[str(r["rating"])] = r["count"]

        return ratings


    # ================= GET DOCTORS BY STATUS =================
    @staticmethod
    def get_doctors_by_status(status):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT id, name, email, location, status
            FROM doctors
            WHERE status=%s
            ORDER BY created_at DESC
        """, (status,))

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results


    # ================= APPROVE DOCTOR =================
    @staticmethod
    def approve_doctor(doctor_id, employee_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE doctors
            SET status='approved',
                employee_id=%s
            WHERE id=%s
        """, (employee_id, doctor_id))

        conn.commit()

        cur.close()
        conn.close()


    # ================= REJECT DOCTOR =================
    @staticmethod
    def reject_doctor(doctor_id, reason):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE doctors
            SET status='rejected',
                rejection_reason=%s
            WHERE id=%s
        """, (reason, doctor_id))

        conn.commit()

        cur.close()
        conn.close()


    # ================= STATS COUNTS =================
    @staticmethod
    def get_doctor_counts():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(status='pending'),0) AS pending,
                COALESCE(SUM(status='approved'),0) AS approved,
                COALESCE(SUM(status='rejected'),0) AS rejected
            FROM doctors
        """)

        result = cur.fetchone()

        cur.close()
        conn.close()

        return result
    @staticmethod
    def get_doctor_full(doctor_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT *
            FROM doctors
            WHERE id=%s
        """, (doctor_id,))

        doctor = cur.fetchone()

        cur.close()
        conn.close()

        return doctor
