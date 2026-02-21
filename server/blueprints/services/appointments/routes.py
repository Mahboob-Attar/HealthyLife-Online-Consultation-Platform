from flask import Blueprint, request, jsonify, render_template, session
from server.blueprints.services.appointments.service import AppointmentService

appointments = Blueprint("appointments", __name__, url_prefix="/appointments")


# ======================================================
# 📄 APPOINTMENT PAGE
# ======================================================
@appointments.route("/", methods=["GET"])
def appointment_page():

    if not session.get("logged_in"):
        return render_template("unauthorized.html"), 401

    return render_template("appointment.html")


# ======================================================
# 👨‍⚕️ GET ALL DOCTORS
# ======================================================
@appointments.route("/api/doctors", methods=["GET"])
def get_doctors():

    result = AppointmentService.load_doctors()
    return jsonify(result)


# ======================================================
# 🔎 SEARCH DOCTORS
# ======================================================
@appointments.route("/api/doctors/search", methods=["GET"])
def search_doctors():

    query = request.args.get("q", "")
    result = AppointmentService.load_doctors(query)

    return jsonify(result)


# ======================================================
# 📅 GET AVAILABILITY
# ======================================================
@appointments.route("/api/availability/<employee_id>", methods=["GET"])
def availability(employee_id):

    result = AppointmentService.get_availability(employee_id)
    return jsonify(result)


# ======================================================
# 📌 BOOK APPOINTMENT
# ======================================================
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