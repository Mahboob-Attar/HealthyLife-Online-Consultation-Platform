from flask import Blueprint, render_template, session, jsonify
from server.blueprints.services.admin.service import AdminService
from server.config.db import get_connection

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# ================= ROLE CHECK =================
def get_role():
    return session.get("role", "").lower()

def is_admin():
    return get_role() == "admin"

# ================= DASHBOARD PAGE =================
@dashboard.route("/")
def dashboard_page():

    role = get_role()
    admin_status = role == "admin"

    return render_template(
        "dashboard.html",
        is_admin=admin_status
    )

# ================= DASHBOARD DATA API =================
@dashboard.route("/data")
def dashboard_data():

    role = get_role()

    # ===== COMMON DATA FOR EVERYONE =====
    stats = AdminService.get_dashboard_stats()
    ratings = AdminService.get_feedback_ratings()

    response_data = {
        "stats": stats,
        "ratings": ratings
    }

    # ===== ADMIN ONLY DATA =====
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
        "role": role if role else "guest",
        "data": response_data
    })
