from datetime import datetime, timedelta
import re
import threading
import logging
from flask import render_template

from server.config.email import send_email_html
from server.blueprints.services.availability.model import AvailabilityModel

logger = logging.getLogger(__name__)


# ================= BACKGROUND EMAIL =================
def send_email_background(email, subject, html):
    try:
        send_email_html(email, subject, html)
    except Exception as e:
        logger.error(f"Availability email failed for {email}: {e}")


class AvailabilityService:

    # ================= ROUND TO HALF HOUR GRID =================
    @staticmethod
    def round_up_to_half_hour(dt):
        minute = dt.minute

        if minute in (0, 30):
            return dt.replace(second=0, microsecond=0)

        if minute < 30:
            return dt.replace(minute=30, second=0, microsecond=0)

        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt + timedelta(hours=1)

    # ================= SAVE AVAILABILITY =================
    @staticmethod
    def save(employee_id, date, start_time, end_time):

        # -------- REQUIRED CHECK --------
        if not all([employee_id, date, start_time, end_time]):
            return False, "All fields are required"

        employee_id = employee_id.strip()

        if not re.match(r"^[A-Za-z0-9\-]+$", employee_id):
            return False, "Invalid Platform Employee ID"

        # -------- CHECK DOCTOR EXISTS --------
        doctor = AvailabilityModel.get_doctor(employee_id)
        if doctor is None:
            return False, "Platform ID not found or not approved"

        doctor_info = AvailabilityModel.get_doctor_email_and_name(employee_id)

        # -------- PARSE TIME --------
        try:
            start_datetime = datetime.strptime(
                f"{date} {start_time}", "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{date} {end_time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            return False, "Invalid time format"

        if start_datetime == end_datetime:
            return False, "Start and end time cannot be same"

        # -------- ROUND TIME --------
        start_datetime = AvailabilityService.round_up_to_half_hour(start_datetime)
        end_datetime = AvailabilityService.round_up_to_half_hour(end_datetime)

        # Overnight case
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)

        if start_datetime < datetime.now():
            return False, "Cannot set availability in the past"

        # -------- CHECK CONFLICT --------
        conflict = AvailabilityModel.check_conflict(
            employee_id, start_datetime, end_datetime
        )

        if conflict:
            return False, "This time slot overlaps with existing availability"

        # -------- SAVE TO DB --------
        AvailabilityModel.insert_availability(
            employee_id, start_datetime, end_datetime
        )

        # -------- SEND EMAIL (NON-BLOCKING) --------
        if doctor_info:
            try:
                html = render_template(
                    "emails/availability_saved_email.html",
                    doctor_name=doctor_info["name"],
                    start_time=start_datetime.strftime("%d %b %Y %I:%M %p"),
                    end_time=end_datetime.strftime("%d %b %Y %I:%M %p"),
                    year=datetime.now().year
                )

                threading.Thread(
                    target=send_email_background,
                    args=(
                        doctor_info["email"],
                        "Availability Confirmed — HealthyLife",
                        html
                    ),
                    daemon=True
                ).start()

            except Exception as e:
                logger.error(f"Availability email template error: {e}")

        return True, "Availability saved successfully"