import os
from flask import Blueprint, render_template, jsonify, session, request
from server.blueprints.services.admin.service import AdminService

admin = Blueprint("admin_bp", __name__, url_prefix="/admin")


# ---------------- AUTH GUARD ----------------
def admin_required():
    return session.get("logged_in") is True and session.get("role") == "admin"


# ---------------- ADMIN LOGIN ----------------
@admin.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if email == admin_email and password == admin_password:
        session.clear()
        session["logged_in"] = True
        session["role"] = "admin"
        return jsonify({"status": "success"})

    return jsonify({"status": "error", "msg": "Invalid admin credentials"})



