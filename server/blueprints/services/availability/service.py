from datetime import datetime, timedelta
import re
from flask import render_template
from server.config.email import send_email_html
from server.blueprints.services.availability.model import AvailabilityModel


class AvailabilityService:

    # ================= ROUND TO HALF HOUR GRID =================
    @staticmethod
    def round_up_to_half_hour(dt):

        minute = dt.minute

        if minute == 0 or minute == 30:
            return dt.replace(second=0, microsecond=0)

        if minute < 30:
            return dt.replace(minute=30, second=0, microsecond=0)

        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt + timedelta(hours=1)

    # ================= SAVE AVAILABILITY =================
    @staticmethod
    def save(employee_id, date, start_time, end_time):

        if not employee_id or not date or not start_time or not end_time:
            return False, "All fields are required"

        employee_id = employee_id.strip()

        if not re.match(r"^[A-Za-z0-9\-]+$", employee_id):
            return False, "Invalid Platform Employee ID"

        # CHECK DOCTOR EXISTS
        doctor = AvailabilityModel.get_doctor(employee_id)
        if doctor is None:
            return False, "Platform ID not found or not approved"

        # GET EMAIL + NAME
        doctor_info = AvailabilityModel.get_doctor_email_and_name(employee_id)

        # PARSE TIMES
        try:
            start_obj = datetime.strptime(start_time, "%H:%M")
            end_obj = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            return False, "Invalid time format"

        if start_obj == end_obj:
            return False, "Start and end time cannot be same"

        start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        start_datetime = AvailabilityService.round_up_to_half_hour(start_datetime)
        end_datetime = AvailabilityService.round_up_to_half_hour(end_datetime)

        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)

        if start_datetime < datetime.now():
            return False, "Cannot set availability in the past"

        conflict = AvailabilityModel.check_conflict(
            employee_id, start_datetime, end_datetime
        )

        if conflict:
            return False, "This time slot overlaps with existing availability"

        # SAVE
        AvailabilityModel.insert_availability(
            employee_id, start_datetime, end_datetime
        )

        # ================= SEND EMAIL =================
        try:
            if doctor_info:

                html = render_template(
                    "emails/availability_saved_email.html",
                    doctor_name=doctor_info["name"],
                    start_time=start_datetime.strftime("%d %b %Y %I:%M %p"),
                    end_time=end_datetime.strftime("%d %b %Y %I:%M %p"),
                    year=datetime.now().year
                )

                send_email_html(
                    doctor_info["email"],
                    "Availability Confirmed — HealthyLife",
                    html
                )

        except Exception as e:
            print("EMAIL ERROR:", e)

        return True, "Availability saved successfully"