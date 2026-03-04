from server.config.db import get_connection


class DoctorModel:
    """
    Handles all database operations related to doctors.
    Model layer = DB only.
    """

    # Check email exists
    @staticmethod
    def find_by_email(email: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM doctors WHERE email=%s LIMIT 1", (email,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists

    # Check license email exists
    @staticmethod
    def find_by_license(license_email: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM doctors WHERE license_email=%s LIMIT 1",
            (license_email,)
        )
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists

    # Check phone exists
    @staticmethod
    def find_by_phone(phone: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM doctors WHERE phone=%s LIMIT 1", (phone,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists

    # Create doctor (FIXED)
    @staticmethod
    def create(data: dict) -> bool:
        conn = get_connection()
        cur = conn.cursor()

        try:
            sql = """
                INSERT INTO doctors
                (
                    name,
                    phone,
                    email,
                    license_email,
                    specialization,
                    experience,
                    clinic,
                    location,
                    services,
                    photo_path
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cur.execute(sql, (
                data["name"],
                data["phone"],
                data["email"],
                data["license_email"],
                data["specialization"],
                data["experience"],
                data["clinic"],
                data["location"],
                data["services"],
                data["photo_path"]
            ))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("DoctorModel.create Error:", e)
            return False

        finally:
            cur.close()
            conn.close()

    # Get all doctors (public list)
    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT
                id,
                name,
                specialization,
                clinic,
                location,
                photo_path
            FROM doctors
            WHERE status = 'approved'
            ORDER BY created_at DESC
        """)

        doctors = cur.fetchall()
        cur.close()
        conn.close()
        return doctors
