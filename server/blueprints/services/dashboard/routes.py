from flask import Blueprint, render_template, session, jsonify
from server.blueprints.services.admin.service import AdminService
from server.config.db import get_connection

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# ================= LOGIN CHECK =================
def login_required():
    return session.get("logged_in") is True


# ================= DASHBOARD PAGE =================
@dashboard.route("/")
def dashboard_page():

    # If not logged in → show unauthorized page
    if not login_required():
        return render_template("unauthorized.html"), 403

    # Get role safely
    role = session.get("role", "").lower()

    # Determine admin
    is_admin = role == "admin"

    return render_template(
        "dashboard.html",
        is_admin=is_admin
    )


# ================= DASHBOARD DATA API =================
@dashboard.route("/data")
def dashboard_data():

    # API should return JSON if not logged
    if not login_required():
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    role = session.get("role", "").lower()

    # ===== COMMON DATA FOR BOTH ROLES =====
    stats = AdminService.get_dashboard_stats()
    ratings = AdminService.get_feedback_ratings()

    response_data = {
        "stats": stats,
        "ratings": ratings
    }

    # ===== ADMIN EXTRA DATA =====
    if role == "admin":
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT id, name, email, created_at FROM users")
        users = cur.fetchall()

        cur.close()
        conn.close()

        response_data["users"] = users

    return jsonify({
        "success": True,
        "role": role,
        "data": response_data
    })
