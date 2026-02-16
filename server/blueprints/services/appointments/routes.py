from flask import Blueprint, request, render_template, jsonify, session
from server.blueprints.services.appointments.service import AppointmentService

appointments = Blueprint("appointments", __name__, url_prefix="/appointments")


# ================= PAGE ROUTE =================
@appointments.route("/", methods=["GET"])
def appointment_page():

    # 🔐 Proper login check
    if not session.get("logged_in"):
        return render_template("unauthorized.html"), 401
    # ===== UNKNOWN ROLE =====
    else:
        return render_template("unauthorized.html"), 403
