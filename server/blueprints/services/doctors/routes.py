import re
import logging
from flask import Blueprint, request, jsonify, send_from_directory

from server.blueprints.services.doctors.service import DoctorService

logger = logging.getLogger(__name__)

doctors = Blueprint("doctors_bp", __name__, url_prefix="/doctors")


# ================= LICENSE REGEX =================
LICENSE_REGEX = r"^[A-Z]{3}[0-9]{3}@gov\.ac\.in$"


# ================= VERIFY LICENSE =================
@doctors.route("/verify-license", methods=["POST"])
def verify_license():
    try:
        data = request.get_json()

        if not data or "license" not in data:
            return jsonify({
                "success": False,
                "message": "License email required"
            }), 400

        license_email = data.get("license").strip()

        if not re.match(LICENSE_REGEX, license_email):
            return jsonify({
                "success": False,
                "message": "Invalid Government License format"
            }), 400

        return jsonify({
            "success": True,
            "message": "License format valid"
        }), 200

    except Exception as e:
        logger.error(f"Verify license error: {e}")
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# ================= REGISTER DOCTOR =================
@doctors.route("/register", methods=["POST"])
def register_doctor():
    try:
        response = DoctorService.register(request)

        return jsonify({
            "success": response.get("success"),
            "message": response.get("message")
        }), response.get("status", 500)

    except Exception as e:
        logger.error(f"Register doctor error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500


# ================= GET ALL DOCTORS =================
@doctors.route("/all", methods=["GET"])
def get_doctors():
    try:
        doctors = DoctorService.get_all()
        return jsonify({"success": True, "doctors": doctors}), 200

    except Exception as e:
        logger.error(f"Get doctors error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500


# ================= SERVE IMAGE =================
@doctors.route("/image/<filename>")
def doctor_image(filename):
    try:
        file_path = DoctorService.get_image_path()
        return send_from_directory(file_path, filename)

    except Exception as e:
        logger.error(f"Image serve error: {e}")
        return "Image not found", 404
