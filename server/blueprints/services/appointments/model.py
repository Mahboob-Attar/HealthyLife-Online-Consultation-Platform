from server.config.db import get_connection


class AppointmentModel:

    # ================= CLEAN EXPIRED AVAILABILITY =================
    @staticmethod
    def delete_expired_availability():
        db = get_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                DELETE FROM doctor_availability
                WHERE end_datetime < NOW()
            """)
            db.commit()
        finally:
            cursor.close()
            db.close()

    # ================= GET AVAILABLE DOCTORS =================
    @staticmethod
    def get_available_doctors():

        AppointmentModel.delete_expired_availability()

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT 
                    d.employee_id,
                    d.name,
                    d.specialization,
                    d.experience,
                    d.photo_path,
                    MIN(da.start_datetime) AS next_slot
                FROM doctors d
                JOIN doctor_availability da
                    ON d.employee_id = da.employee_id
                WHERE d.status='approved'
                AND da.start_datetime > NOW()
                GROUP BY d.employee_id
                ORDER BY next_slot ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()

    # ================= SEARCH AVAILABLE DOCTORS =================
    @staticmethod
    def search_available_doctors(search_query):

        AppointmentModel.delete_expired_availability()

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        search = f"%{search_query}%"

        try:
            cursor.execute("""
                SELECT 
                    d.employee_id,
                    d.name,
                    d.specialization,
                    d.experience,
                    d.photo_path,
                    MIN(da.start_datetime) AS next_slot
                FROM doctors d
                JOIN doctor_availability da
                    ON d.employee_id = da.employee_id
                WHERE d.status='approved'
                AND da.start_datetime > NOW()
                AND (
                    d.specialization LIKE %s
                    OR d.services LIKE %s
                    OR d.name LIKE %s
                )
                GROUP BY d.employee_id
                ORDER BY next_slot ASC
            """, (search, search, search))

            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()

    # ================= GET DOCTOR AVAILABILITY =================
    @staticmethod
    def get_doctor_availability(employee_id):

        AppointmentModel.delete_expired_availability()

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT start_datetime, end_datetime
                FROM doctor_availability
                WHERE employee_id=%s
                AND start_datetime > NOW()
                ORDER BY start_datetime
            """, (employee_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            db.close()

    # ================= CHECK IF TIME BOOKED =================
    @staticmethod
    def is_time_booked(employee_id, appointment_datetime):

        db = get_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM appointments
                WHERE employee_id=%s
                AND appointment_datetime=%s
            """, (employee_id, appointment_datetime))

            return cursor.fetchone()[0] > 0

        finally:
            cursor.close()
            db.close()

    # ================= CHECK WITHIN AVAILABILITY =================
    @staticmethod
    def is_within_availability(employee_id, appointment_datetime):

        db = get_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM doctor_availability
                WHERE employee_id=%s
                AND %s BETWEEN start_datetime AND end_datetime
            """, (employee_id, appointment_datetime))

            return cursor.fetchone()[0] > 0

        finally:
            cursor.close()
            db.close()

    # ================= CREATE APPOINTMENT =================
    @staticmethod
    def create_appointment(user_id, employee_id, appointment_datetime, meeting_link):

        db = get_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                INSERT INTO appointments
                (user_id, employee_id, appointment_datetime, meeting_link)
                VALUES (%s, %s, %s, %s)
            """, (user_id, employee_id, appointment_datetime, meeting_link))

            db.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            db.close()

    # ================= GET USER DETAILS =================
    @staticmethod
    def get_user_details(user_id):

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT name, email
                FROM users
                WHERE id=%s
            """, (user_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            db.close()

    # ================= GET DOCTOR DETAILS =================
    @staticmethod
    def get_doctor_details(employee_id):

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT name, email, specialization
                FROM doctors
                WHERE employee_id=%s
            """, (employee_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            db.close()