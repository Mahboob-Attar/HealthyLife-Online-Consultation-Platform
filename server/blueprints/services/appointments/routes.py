from flask import Blueprint, request,render_template, jsonify, session
appointments = Blueprint("appointments", __name__, url_prefix="/appointments")


@appointments.route("/", methods=["GET"])
def appointment_page():

    #  Not logged in
    if not session.get("logged_in"):
        return render_template("unauthorized.html"), 401

    #  Admin should not book
    role = session.get("role", "").lower()
    if role == "admin":
            return jsonify({
                "success": False,
                "message": "Admin cannot submit feedback"
            }), 403


    #  Only user allowed
    return render_template("appointment.html")