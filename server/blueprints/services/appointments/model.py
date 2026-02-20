from server.config.db import get_connection

class AppointmentModel:

    @staticmethod
    def get_all_doctors():
        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT *
        FROM doctors
        WHERE status='approved'
        ORDER BY experience DESC
        """

        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def search_doctors(query):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        sql = """
        SELECT *
        FROM doctors
        WHERE status='approved'
        AND (
            specialization LIKE %s
            OR services LIKE %s
        )
        ORDER BY experience DESC
        """

        search = f"%{query}%"
        cursor.execute(sql, (search, search))

        return cursor.fetchall()