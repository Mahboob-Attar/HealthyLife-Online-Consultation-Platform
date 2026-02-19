from datetime import datetime, timedelta
import re
from server.blueprints.services.availability.model import AvailabilityModel


class AvailabilityService:

    @staticmethod
    def save(employee_id, date, start_time, end_time):

        # REQUIRED FIELDS
        if not employee_id or not date or not start_time or not end_time:
            return False, "All fields are required"

        employee_id = employee_id.strip()

        # ID FORMAT
        if not re.match(r"^[A-Za-z0-9\-]+$", employee_id):
            return False, "Invalid Platform Employee ID"

        # CHECK DOCTOR EXISTS
        doctor = AvailabilityModel.get_doctor(employee_id)
        if doctor is None:
            return False, "Platform ID not found or not approved"

        # PARSE TIMES
        try:
            start_obj = datetime.strptime(start_time, "%H:%M")
            end_obj = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            return False, "Invalid time format"

        # SAME TIME NOT ALLOWED
        if start_obj == end_obj:
            return False, "Start and end time cannot be same"

        # CREATE FULL DATETIME
        start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        # OVERNIGHT SHIFT SUPPORT
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)

        # PAST CHECK
        if start_datetime < datetime.now():
            return False, "Cannot set availability in the past"

        #  CONFLICT CHECK (IMPORTANT)
        conflict = AvailabilityModel.check_conflict(
            employee_id, start_datetime, end_datetime
        )

        if conflict:
            return False, "This time slot overlaps with existing availability"

        # SAVE
        AvailabilityModel.insert_availability(
            employee_id, start_datetime, end_datetime
        )

        return True, "Availability saved successfully"
