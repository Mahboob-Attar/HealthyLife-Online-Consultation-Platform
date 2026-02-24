from server.blueprints.services.appointments.model import AppointmentModel
from server.config.email import send_email_html
from flask import render_template
from datetime import datetime
import uuid
import time


_search_last_call = {}
SEARCH_COOLDOWN = 0.5


class AppointmentService:

    # ================= LOAD AVAILABLE DOCTORS =================
    @staticmethod
    def get_available_doctors():

        try:
            doctors = AppointmentModel.get_available_doctors()

            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
                doc["photo_url"] = f"/uploads/doctors/{doc['photo_path']}"

            return doctors

        except Exception as e:
            print("AVAILABLE ERROR:", e)
            return []

    # ================= SEARCH AVAILABLE DOCTORS =================
    @staticmethod
    def search_available_doctors(search_query):

        try:
            user_key = "global"
            now = time.time()

            if now - _search_last_call.get(user_key, 0) < SEARCH_COOLDOWN:
                return []

            _search_last_call[user_key] = now

            doctors = AppointmentModel.search_available_doctors(search_query)

            for doc in doctors:
                doc["photo_path"] = doc.get("photo_path") or "default.jpg"
                doc["photo_url"] = f"/uploads/doctors/{doc['photo_path']}"

            return doctors

        except Exception as e:
            print("SEARCH ERROR:", e)
            return []

    # ================= GET AVAILABILITY =================
    @staticmethod
    def get_availability(employee_id):

        try:
            slots = AppointmentModel.get_doctor_availability(employee_id)
            return {"success": True, "data": slots}

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ================= BOOK APPOINTMENT =================
    @staticmethod
    def book_appointment(user_id, employee_id, appointment_datetime):

        try:

            # 🔹 Convert string to datetime
            appointment_datetime = datetime.fromisoformat(appointment_datetime)

            if not AppointmentModel.is_within_availability(employee_id, appointment_datetime):
                return {"success": False, "error": "Doctor not available at this time"}

            if AppointmentModel.is_time_booked(employee_id, appointment_datetime):
                return {"success": False, "error": "Slot already booked"}

            meeting_link = f"https://meet.jit.si/healthylife-{uuid.uuid4()}"

            appointment_id = AppointmentModel.create_appointment(
                user_id,
                employee_id,
                appointment_datetime,
                meeting_link
            )

            # ================= FETCH DETAILS =================
            user = AppointmentModel.get_user_details(user_id)
            doctor = AppointmentModel.get_doctor_details(employee_id)

            date_str = appointment_datetime.strftime("%d %B %Y")
            time_str = appointment_datetime.strftime("%I:%M %p")

            # ================= USER EMAIL =================
            try:
                user_html = render_template(
                    "emails/appointment_user_email.html",
                    user_name=user["name"],
                    doctor_name=doctor["name"],
                    specialization=doctor["specialization"],
                    date=date_str,
                    time=time_str,
                    meeting_url=meeting_link,
                    year=datetime.now().year
                )

                send_email_html(user["email"], "Appointment Confirmed", user_html)
            except Exception as e:
                print("USER EMAIL ERROR:", e)

            # ================= DOCTOR EMAIL =================
            try:
                doctor_html = render_template(
                    "emails/appointment_doctor_email.html",
                    user_name=user["name"],
                    doctor_name=doctor["name"],
                    specialization=doctor["specialization"],
                    date=date_str,
                    time=time_str,
                    meeting_url=meeting_link,
                    year=datetime.now().year
                )

                send_email_html(doctor["email"], "New Consultation Assigned", doctor_html)
            except Exception as e:
                print("DOCTOR EMAIL ERROR:", e)

            return {
                "success": True,
                "message": "Appointment booked successfully",
                "meeting_link": meeting_link,
                "appointment_id": appointment_id
            }

        except Exception as e:
            print("BOOK ERROR:", e)
            return {"success": False, "error": str(e)}