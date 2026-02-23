from flask import Blueprint, request, jsonify, render_template, session
from server.blueprints.services.appointments.service import AppointmentService

appointments = Blueprint("appointments", __name__, url_prefix="/appointments")


#  APPOINTMENT PAGE
@appointments.route("/", methods=["GET"])
def appointment_page():

    if not session.get("logged_in"):
        return render_template("unauthorized.html"), 401

    return render_template("appointment.html")


# GET AVAILABLE + RECENT DOCTORS
@appointments.route("/api/doctors", methods=["GET"])
def get_doctors():

    result = {
        "available": AppointmentService.get_available_doctors(),
        "recent": AppointmentService.get_recent_doctors()
    }

    return jsonify(result)


# EARCH AVAILABLE DOCTORS ONLY
@appointments.route("/api/doctors/search", methods=["GET"])
def search_doctors():

    query = request.args.get("q", "")
    result = AppointmentService.search_available_doctors(query)

    return jsonify({
        "available": result,
        "recent": []
    })


#  GET AVAILABILITY
@appointments.route("/api/availability/<employee_id>", methods=["GET"])
def availability(employee_id):

    result = AppointmentService.get_availability(employee_id)
    return jsonify(result)


# BOOK APPOINTMENT
@appointments.route("/api/book", methods=["POST"])
def book():

    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "error": "Not logged in"
        }), 401

    data = request.json

    result = AppointmentService.book_appointment(
        session.get("user_id"),
        data.get("employee_id"),
        data.get("datetime")
    )

    return jsonify(result)