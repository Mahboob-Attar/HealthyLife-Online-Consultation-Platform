from server.blueprints.services.appointments.model import AppointmentModel
import uuid


class AppointmentService:
    """
    Business logic layer for appointment system
    Handles doctor loading, availability, and booking
    """

    # ======================================================
    #  LOAD DOCTORS
    # ======================================================
    @staticmethod
    def load_doctors(search_query=None):

        try:
            if search_query:
                doctors = AppointmentModel.search_doctors(search_query)
            else:
                doctors = AppointmentModel.get_all_doctors()

            # Photo fallback + URL
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

            #  Validate within availability window FIRST
            if not AppointmentModel.is_within_availability(employee_id, appointment_datetime):
                return {
                    "success": False,
                    "error": "Selected time is outside doctor availability"
                }

            #  Check conflict
            if AppointmentModel.is_time_booked(employee_id, appointment_datetime):
                return {
                    "success": False,
                    "error": "Selected time is already booked"
                }

            #  Generate meeting link
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