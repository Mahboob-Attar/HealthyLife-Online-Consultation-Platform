from flask import Blueprint, request, jsonify
from blueprints.services.availability.service import AvailabilityService

availability = Blueprint("availability", __name__, url_prefix="/availability")


@availability.route("/save", methods=["POST"])
def save():

    employee_id = request.form.get("employee_id")
    date = request.form.get("date")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    success, message = AvailabilityService.save(
        employee_id, date, start_time, end_time
    )

    status_code = 200 if success else 400

    return jsonify({
        "success": success,
        "message": message
    }), status_code
