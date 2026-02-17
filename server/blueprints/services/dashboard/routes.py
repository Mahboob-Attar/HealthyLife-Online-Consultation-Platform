from flask import Blueprint, render_template, session, jsonify, request
from functools import wraps
import logging
from flask import send_file
from server.blueprints.services.dashboard.service import DashboardService
from server.config.db import get_connection

logger = logging.getLogger(__name__)

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# ============================================================
# ================= ROLE HELPERS =============================
# ============================================================

def get_role():
    return session.get("role", "").lower()

def is_admin():
    return get_role() == "admin"

def is_logged_in():
    return session.get("logged_in") is True


# ============================================================
# ================= DECORATORS ===============================
# ============================================================

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return jsonify({"success": False, "message": "Login required"}), 401
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_admin():
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return wrapper


# ============================================================
# ================= DASHBOARD PAGE ===========================
# ============================================================

@dashboard.route("/")
def dashboard_page():

    return render_template(
        "dashboard.html",
        is_admin=is_admin(),
        role=get_role() if get_role() else "guest"
    )


# ============================================================
# ================= DASHBOARD DATA ===========================
# ============================================================

@dashboard.route("/data")
def dashboard_data():

    role = get_role()

    stats = DashboardService.get_dashboard_stats()
    ratings = DashboardService.get_feedback_ratings()

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
        "role": role if role else "guest",
        "data": response_data
    })


# ============================================================
# ================= ADMIN DOCTOR APIs ========================
# ============================================================

# ================= GET DOCTORS =================
@dashboard.route("/admin/doctors")
@admin_required
def get_doctors():

    status = request.args.get("status", "pending")

    doctors = DashboardService.get_doctors(status)

    return jsonify({
        "success": True,
        "doctors": doctors
    })


# ================= APPROVE DOCTOR =================
@dashboard.route("/admin/doctors/<int:doctor_id>/approve", methods=["POST"])
@admin_required
def approve_doctor(doctor_id):

    success = DashboardService.approve_doctor(doctor_id)

    return jsonify({
        "success": success,
        "message": "Doctor approved" if success else "Approval failed"
    })


# ================= REJECT DOCTOR =================
@dashboard.route("/admin/doctors/<int:doctor_id>/reject", methods=["POST"])
@admin_required
def reject_doctor(doctor_id):

    data = request.get_json()
    reason = data.get("reason")

    if not reason:
        return jsonify({"success": False, "message": "Reason required"}), 400

    success = DashboardService.reject_doctor(doctor_id, reason)

    return jsonify({
        "success": success,
        "message": "Doctor rejected" if success else "Reject failed"
    })


# ================= APPROVAL STATS =================
@dashboard.route("/admin/doctors/stats")
@admin_required
def approval_stats():

    stats = DashboardService.get_stats()

    return jsonify(stats)


@dashboard.route("/admin/doctors/<int:doctor_id>/pdf")
def doctor_pdf(doctor_id):

    if not is_admin():
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    pdf_path = DashboardService.generate_doctor_pdf(doctor_id)

    return send_file(pdf_path, as_attachment=False)
