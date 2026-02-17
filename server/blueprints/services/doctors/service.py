import os
import re
import uuid
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template

from server.blueprints.services.doctors.model import DoctorModel
from server.config.email import send_email_html

UPLOAD_FOLDER = "uploads/doctors"
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

# Allowed cities
ALLOWED_CITIES = {
    "Bangalore South",
    "Bangalore North",
    "Bangalore Urban",
    "Bangalore Rural"
}

LICENSE_REGEX = r"^[A-Z]{3}[0-9]{3}@gov\.ac\.in$"
PHONE_REGEX = r"^\+?\d{10,15}$"
EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"

logger = logging.getLogger(__name__)


class DoctorService:

    @staticmethod
    def get_image_path():
        return UPLOAD_FOLDER

    # ================= REGISTER =================
    @staticmethod
    def register(request):
        try:
            form = request.form

            name = form.get("name")
            phone = form.get("phone")
            email = form.get("email")
            license_email = form.get("license")
            specialization = form.get("specialization")
            experience = form.get("experience")
            services = form.get("services")
            clinic = form.get("clinic")
            location = form.get("location")
            user_id = form.get("user_id")

            photo = request.files.get("photo")

            # ================= REQUIRED CHECK =================
            if not all([
                name, phone, email, license_email,
                specialization, experience, services,
                clinic, location, photo
            ]):
                return {
                    "success": False,
                    "message": "All fields are required",
                    "status": 400
                }

            # ================= FORMAT VALIDATION =================
            if not re.match(PHONE_REGEX, phone):
                return {"success": False, "message": "Invalid phone number", "status": 400}

            if not re.match(EMAIL_REGEX, email):
                return {"success": False, "message": "Invalid email", "status": 400}

            if not re.match(LICENSE_REGEX, license_email):
                return {"success": False, "message": "Invalid government license", "status": 400}

            if location not in ALLOWED_CITIES:
                return {"success": False, "message": "Invalid city selected", "status": 400}

            try:
                exp = int(experience)
                if exp < 0:
                    raise ValueError
            except:
                return {"success": False, "message": "Invalid experience", "status": 400}

            # ================= DUPLICATE CHECK =================
            if DoctorModel.find_by_email(email):
                return {"success": False, "message": "Email already registered", "status": 409}

            if DoctorModel.find_by_phone(phone):
                return {"success": False, "message": "Phone already registered", "status": 409}

            if DoctorModel.find_by_license(license_email):
                return {"success": False, "message": "License already registered", "status": 409}

            # ================= IMAGE VALIDATION =================
            if "." not in photo.filename:
                return {"success": False, "message": "Invalid image file", "status": 400}

            ext = photo.filename.rsplit(".", 1)[1].lower()

            if ext not in ALLOWED_EXT:
                return {"success": False, "message": "Unsupported image type", "status": 400}

            # ================= SAVE IMAGE =================
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
            photo_path = os.path.join(UPLOAD_FOLDER, filename)

            photo.save(photo_path)

            # ================= CREATE DB =================
            created = DoctorModel.create({
                "user_id": user_id,
                "name": name,
                "phone": phone,
                "email": email,
                "license_email": license_email,
                "experience": exp,
                "specialization": specialization,
                "services": services,
                "clinic": clinic,
                "location": location,
                "photo_path": filename
            })

            if not created:
                if os.path.exists(photo_path):
                    os.remove(photo_path)

                return {
                    "success": False,
                    "message": "Registration failed",
                    "status": 500
                }

            # ================= EMAIL =================
            try:
                html = render_template(
                    "emails/doctor_registration_email.html",
                    doctor_name=name,
                    specialization=specialization,
                    clinic=clinic,
                    location=location,
                    experience=exp,
                    year=datetime.now().year
                )

                email_sent = send_email_html(
                    email,
                    "Doctor Registration Received",
                    html
                )

                if not email_sent:
                    logger.warning(f"Email sending failed for {email}")

            except Exception as mail_error:
                logger.error(f"Email error for {email}: {mail_error}")

            return {
                "success": True,
                "message": "Registration submitted successfully",
                "status": 200
            }

        except Exception as e:
            logger.error(f"DoctorService.register Error: {e}")

            return {
                "success": False,
                "message": "Internal server error",
                "status": 500
            }

    # ================= GET ALL =================
    @staticmethod
    def get_all():
        return DoctorModel.get_all()
