from flask import Blueprint, request, jsonify, render_template, session
from server.blueprints.services.appointments.service import AppointmentService

appointments = Blueprint("appointments", __name__, url_prefix="/appointments")


# ================= PAGE =================
@appointments.route("/", methods=["GET"])
def appointment_page():

    if not session.get("logged_in"):
        return render_template("unauthorized.html"), 401

    return render_template("appointment.html")


# ================= GET AVAILABLE DOCTORS =================
@appointments.route("/api/doctors", methods=["GET"])
def get_doctors():

    try:
        doctors = AppointmentService.get_available_doctors()

        if not doctors:
            return jsonify({
                "success": True,
                "message": "No doctors available at this time",
                "available": []
            })

        return jsonify({
            "success": True,
            "available": doctors
        })

    except Exception as e:
        print("DOCTORS ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ================= SEARCH DOCTORS =================
@appointments.route("/api/doctors/search", methods=["GET"])
def search_doctors():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "error": "Search query required"
        }), 400

    try:
        doctors = AppointmentService.search_available_doctors(query)

        if not doctors:
            return jsonify({
                "success": True,
                "message": "No active doctors found for this specialization",
                "available": []
            })

        return jsonify({
            "success": True,
            "available": doctors
        })

    except Exception as e:
        print("SEARCH ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ================= GET AVAILABILITY =================
@appointments.route("/api/availability/<employee_id>", methods=["GET"])
def availability(employee_id):

    try:
        result = AppointmentService.get_availability(employee_id)
        return jsonify(result)

    except Exception as e:
        print("AVAILABILITY ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ================= BOOK APPOINTMENT =================
@appointments.route("/api/book", methods=["POST"])
def book():

    if not session.get("user_id"):
        return jsonify({
            "success": False,
            "error": "User not logged in"
        }), 401

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request body"
        }), 400

    employee_id = data.get("employee_id")
    appointment_datetime = data.get("datetime")

    if not employee_id or not appointment_datetime:
        return jsonify({
            "success": False,
            "error": "Missing required fields"
        }), 400

    try:
        result = AppointmentService.book_appointment(
            session.get("user_id"),
            employee_id,
            appointment_datetime
        )

        return jsonify(result)

    except Exception as e:
        print("BOOK ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500