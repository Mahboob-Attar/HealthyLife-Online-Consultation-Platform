from flask import Blueprint, request, redirect, url_for, flash
from server.blueprints.services.availability.service import AvailabilityService

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

    if not success:
        flash(message, "error")
        return redirect(url_for("home.index"))   

    flash(message, "success")
    return redirect(url_for("home.index"))
