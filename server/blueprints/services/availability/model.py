from server.config.db import get_connection


class AvailabilityModel:

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
    def insert_availability(employee_id, start_datetime, end_datetime):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO doctor_availability
            (employee_id, start_datetime, end_datetime)
            VALUES (%s, %s, %s)
        """, (employee_id, start_datetime, end_datetime))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def check_conflict(employee_id, start_datetime, end_datetime):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id FROM doctor_availability
            WHERE employee_id=%s
            AND (
                (%s < end_datetime AND %s > start_datetime)
            )
        """, (employee_id, start_datetime, end_datetime))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_doctor_email_and_name(employee_id):
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT email, name FROM doctors WHERE employee_id=%s",
                (employee_id,)
            )

            result = cursor.fetchone()

            cursor.close()
            conn.close()

            return result