from server.config.db import get_connection


class AppointmentModel:

    # ======================================================
    # 👨‍⚕️ GET ALL APPROVED DOCTORS
    # ======================================================
    @staticmethod
    def get_all_doctors():
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT employee_id, name, specialization, experience, photo_path
        FROM doctors
        WHERE status='approved'
        ORDER BY experience DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result


    # ======================================================
    # 🔎 SEARCH DOCTORS
    # ======================================================
    @staticmethod
    def search_doctors(search_query):
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        sql = """
        SELECT employee_id, name, specialization, experience, photo_path
        FROM doctors
        WHERE status='approved'
        AND (
            specialization LIKE %s
            OR services LIKE %s
        )
        ORDER BY experience DESC
        """

        search = f"%{search_query}%"
        cursor.execute(sql, (search, search))

        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result


    # ======================================================
    # 📅 GET DOCTOR AVAILABILITY
    # ======================================================
    @staticmethod
    def get_doctor_availability(employee_id):
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT start_datetime, end_datetime
        FROM doctor_availability
        WHERE employee_id=%s
        AND start_datetime > NOW()
        ORDER BY start_datetime
        """

        cursor.execute(query, (employee_id,))
        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result


    # ======================================================
    # 🛑 CHECK IF TIME ALREADY BOOKED
    # ======================================================
    @staticmethod
    def is_time_booked(employee_id, appointment_datetime):
        db = get_connection()
        cursor = db.cursor()

        query = """
        SELECT COUNT(*)
        FROM appointments
        WHERE employee_id=%s
        AND appointment_datetime=%s
        """

        cursor.execute(query, (employee_id, appointment_datetime))
        count = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return count > 0


    # ======================================================
    # ✅ CHECK IF TIME WITHIN AVAILABILITY
    # ======================================================
    @staticmethod
    def is_within_availability(employee_id, appointment_datetime):
        db = get_connection()
        cursor = db.cursor()

        query = """
        SELECT COUNT(*)
        FROM doctor_availability
        WHERE employee_id=%s
        AND %s BETWEEN start_datetime AND end_datetime
        """

        cursor.execute(query, (employee_id, appointment_datetime))
        count = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return count > 0


    # ======================================================
    # 📌 CREATE APPOINTMENT
    # ======================================================
    @staticmethod
    def create_appointment(user_id, employee_id, appointment_datetime, meeting_link):
        db = get_connection()
        cursor = db.cursor()

        query = """
        INSERT INTO appointments (user_id, employee_id, appointment_datetime, meeting_link)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (user_id, employee_id, appointment_datetime, meeting_link))
        db.commit()

        appointment_id = cursor.lastrowid

        cursor.close()
        db.close()

        return appointment_id