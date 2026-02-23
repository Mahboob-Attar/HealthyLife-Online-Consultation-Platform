from server.blueprints.services.appointments.model import AppointmentModel
import uuid
import time


#  Search throttle store
_search_last_call = {}
SEARCH_COOLDOWN = 5

class AppointmentService:
    """
    Business logic layer for appointment system
    Handles doctor loading, availability, and booking
    """

    # ======================================================
    #  LOAD DOCTORS (ALL APPROVED)
    # ======================================================
    @staticmethod
    def load_doctors(search_query=None):

        try:
            if search_query:
                doctors = AppointmentModel.search_doctors(search_query)
            else:
                doctors = AppointmentModel.get_all_doctors()

            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
                doc["photo_url"] = f"/uploads/doctors/{doc['photo_path']}"

            return {
                "success": True,
                "data": doctors
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ======================================================
    # 🟢 GET AVAILABLE DOCTORS
    # ======================================================
    @staticmethod
    def get_available_doctors():

        try:
            doctors = AppointmentModel.get_available_doctors()

            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
                doc["photo_url"] = f"/uploads/doctors/{doc['photo_path']}"

            return doctors

        except Exception:
            return []

    # ======================================================
    # 🆕 GET RECENT DOCTORS
    # ======================================================
    @staticmethod
    def get_recent_doctors():

        try:
            doctors = AppointmentModel.get_recent_doctors()

            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
                doc["photo_url"] = f"/uploads/doctors/{doc['photo_path']}"

            return doctors

        except Exception:
            return []

    # ======================================================
    # 🔎 SEARCH AVAILABLE DOCTORS (THROTTLED)
    # ======================================================
    @staticmethod
    def search_available_doctors(search_query):

        try:
            # 🔒 Use global key (can be changed to session/ip later)
            user_key = "global"

            now = time.time()
            last_call = _search_last_call.get(user_key, 0)

            # Throttle protection
            if now - last_call < SEARCH_COOLDOWN:
                return []

            _search_last_call[user_key] = now

            doctors = AppointmentModel.search_available_doctors(search_query)

            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
                doc["photo_url"] = f"/uploads/doctors/{doc['photo_path']}"

            return doctors

        except Exception:
            return []

    # ======================================================
    # GET AVAILABILITY
    # ======================================================
    @staticmethod
    def get_availability(employee_id):

        try:
            availability = AppointmentModel.get_doctor_availability(employee_id)

            return {
                "success": True,
                "data": availability
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ======================================================
    #  BOOK APPOINTMENT
    # ======================================================
    @staticmethod
    def book_appointment(user_id, employee_id, appointment_datetime):

        try:
            if not employee_id or not appointment_datetime:
                return {
                    "success": False,
                    "error": "Missing required fields"
                }

            if not AppointmentModel.is_within_availability(employee_id, appointment_datetime):
                return {
                    "success": False,
                    "error": "Selected time is outside doctor availability"
                }

            if AppointmentModel.is_time_booked(employee_id, appointment_datetime):
                return {
                    "success": False,
                    "error": "Selected time is already booked"
                }

            meeting_link = f"https://meet.jit.si/healthylife-{uuid.uuid4()}"

            appointment_id = AppointmentModel.create_appointment(
                user_id,
                employee_id,
                appointment_datetime,
                meeting_link
            )

            return {
                "success": True,
                "message": "Appointment booked successfully",
                "appointment_id": appointment_id,
                "meeting_link": meeting_link
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }