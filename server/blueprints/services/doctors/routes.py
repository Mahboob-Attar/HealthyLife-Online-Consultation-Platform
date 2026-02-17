import re
import logging
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from server.blueprints.services.doctors.service import DoctorService

logger = logging.getLogger(__name__)

doctors = Blueprint("doctors_bp", __name__, url_prefix="/doctors")

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
                "message": "Invalid License"
            }), 400

        return jsonify({
            "success": True,
            "message": "License valid"
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
        doctors_list = DoctorService.get_all()
        return jsonify({
            "success": True,
            "doctors": doctors_list
        }), 200

    except Exception as e:
        logger.error(f"Get doctors error: {e}")
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# ================= SERVE IMAGE =================
@doctors.route("/image/<filename>")
def doctor_image(filename):
    try:
        #  Secure filename to prevent path traversal
        filename = secure_filename(filename)

        file_path = DoctorService.get_image_path()

        response = send_from_directory(file_path, filename)

        #  Cache image for 1 day (performance boost)
        response.cache_control.max_age = 86400

        return response

    except Exception as e:
        logger.error(f"Image serve error: {e}")
        return jsonify({
            "success": False,
            "message": "Image not found"
        }), 404
