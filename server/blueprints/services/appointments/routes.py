from flask import Blueprint, render_template, session

appointments = Blueprint("appointments", __name__, url_prefix="/appointments")


@appointments.route("/", methods=["GET"])
def appointment_page():

    #  Not logged in
    if not session.get("logged_in"):
        return render_template("unauthorized.html"), 401

    #  Admin should not book
    if session.get("role") == "admin":
        return render_template("admin_blocked.html"), 403

    #  Only user allowed
    return render_template("appointment.html")