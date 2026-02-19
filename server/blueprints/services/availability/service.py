from server.blueprints.services.availability.model import AvailabilityModel
from datetime import datetime
import re


class AvailabilityService:

    @staticmethod
    def save(employee_id, date, start_time, end_time):

        if not employee_id or not date or not start_time or not end_time:
            return False, "All fields are required"

        employee_id = employee_id.strip()

        # FORMAT CHECK
        if not re.match(r"^[A-Za-z0-9\-]+$", employee_id):
            return False, "Invalid Platform Employee ID"

        # CHECK DOCTOR EXISTS
        doctor = AvailabilityModel.get_doctor(employee_id)

        if doctor is None:
            return False, "Platform ID not found or not approved"

        # VALIDATE DATE TIME
        try:
            selected_datetime = datetime.strptime(
                f"{date} {start_time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            return False, "Invalid date or time format"

        now = datetime.now()

        if selected_datetime < now:
            return False, "Cannot set availability in the past"

        if start_time >= end_time:
            return False, "End time must be after start time"

        # CHECK DUPLICATE
        existing = AvailabilityModel.check_existing(
            employee_id, date, start_time, end_time
        )

        if existing:
            return False, "This slot already exists"

        # SAVE
        AvailabilityModel.insert_availability(
            employee_id, date, start_time, end_time
        )

        return True, "Availability saved successfully"
