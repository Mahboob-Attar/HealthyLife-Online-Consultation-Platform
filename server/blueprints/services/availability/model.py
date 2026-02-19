from server.config.db import get_connection


class AvailabilityModel:

    @staticmethod
    @staticmethod
    def get_doctor(employee_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT employee_id FROM doctors WHERE employee_id=%s AND status='approved'",
            (employee_id,)
        )

        doctor = cursor.fetchone()

        cursor.close()
        conn.close()

        return doctor


    @staticmethod
    def insert_availability(employee_id, date, start_time, end_time):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO doctor_availability
            (employee_id, available_date, start_time, end_time)
            VALUES (%s, %s, %s, %s)
            """,
            (employee_id, date, start_time, end_time)
        )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def check_existing(employee_id, date, start_time, end_time):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id FROM doctor_availability
            WHERE employee_id=%s
            AND available_date=%s
            AND start_time=%s
            AND end_time=%s
        """, (employee_id, date, start_time, end_time))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result
    
    @staticmethod
    def check_conflict(employee_id, date, start_time, end_time):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id FROM doctor_availability
            WHERE employee_id=%s
            AND available_date=%s
            AND (
                (%s BETWEEN start_time AND end_time)
                OR (%s BETWEEN start_time AND end_time)
                OR (start_time BETWEEN %s AND %s)
            )
        """, (employee_id, date, start_time, end_time, start_time, end_time))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result
