import logging
import uuid
import os
from datetime import datetime

from flask import render_template

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

from blueprints.services.dashboard.model import DashboardModel
from config.email import send_email_html

logger = logging.getLogger(__name__)


class DashboardService:

    # ================= DASHBOARD STATS =================
    @staticmethod
    def get_dashboard_stats():
        return {
            "total_doctors": DashboardModel.get_total_doctors(),
            "specializations": DashboardModel.get_specializations()
        }

    # ================= FEEDBACK RATINGS =================
    @staticmethod
    def get_feedback_ratings():
        return {
            "feedback_ratings": DashboardModel.get_feedback_ratings()
        }

    # ================= GET DOCTORS =================
    @staticmethod
    def get_doctors(status):
        return DashboardModel.get_doctors_by_status(status)

    # ================= APPROVE DOCTOR =================
    @staticmethod
    def approve_doctor(doctor_id):

        employee_id = f"HL-{uuid.uuid4().hex[:6].upper()}"
        DashboardModel.approve_doctor(doctor_id, employee_id)

        doctor = DashboardModel.get_doctor_full(doctor_id)

        # generate pdf
        pdf_path = DashboardService.generate_doctor_pdf(doctor_id)

        # render email html
        html = render_template(
            "emails/doctor_approved_email.html",
            doctor_name=doctor["name"],
            year=datetime.now().year
        )

        # send email with attachment
        send_email_html(
            doctor["email"],
            "HealthyLife Registration Approved",
            html,
            attachments=[pdf_path]
        )

        # cleanup temp pdf
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        return True

    # ================= REJECT DOCTOR =================
    @staticmethod
    def reject_doctor(doctor_id, reason):

        DashboardModel.reject_doctor(doctor_id, reason)

        doctor = DashboardModel.get_doctor_full(doctor_id)

        html = render_template(
            "emails/doctor_rejected_email.html",
            doctor_name=doctor["name"],
            reason=reason,
            year=datetime.now().year
        )

        send_email_html(
            doctor["email"],
            "HealthyLife Registration Rejected",
            html
        )

        return True

    # ================= STATS =================
    @staticmethod
    def get_stats():
        return DashboardModel.get_doctor_counts()

    # ================= GENERATE PDF =================
    @staticmethod
    def generate_doctor_pdf(doctor_id):

        doctor = DashboardModel.get_doctor_full(doctor_id)

        if not doctor:
            raise Exception("Doctor not found")

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
        pdf_folder = os.path.join(base_dir, "uploads/pdfs")
        os.makedirs(pdf_folder, exist_ok=True)

        pdf_path = os.path.join(pdf_folder, f"doctor_{doctor_id}.pdf")

        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # HEADER
        c.setFillColor(colors.HexColor("#0f4c81"))
        c.rect(0, height - 80, width, 80, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "HealthyLife Doctor Verification")

        # PHOTO
        photo_x = width - 130
        photo_y = height - 115

        if doctor.get("photo_path"):
            img_path = os.path.join(base_dir, "uploads/doctors", doctor["photo_path"])
            if os.path.exists(img_path):
                c.drawImage(ImageReader(img_path), photo_x, photo_y, 70, 70)

        # APPROVED BADGE
        badge_y = photo_y - 25

        c.setFillColor(colors.HexColor("#2ecc71"))
        c.roundRect(photo_x - 5, badge_y, 80, 20, 4, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(photo_x + 35, badge_y + 6, "APPROVED")

        # INFO BOX
        info_box_top = height - 200
        info_box_height = 260

        c.setFillColor(colors.HexColor("#f5f7fa"))
        c.roundRect(40, info_box_top - info_box_height, width - 80, info_box_height, 10, fill=True, stroke=False)

        c.setFillColor(colors.black)
        c.setFont("Helvetica", 11)

        y = info_box_top - 20

        fields = [
            ("Name", doctor["name"]),
            ("Email", doctor["email"]),
            ("Phone", doctor["phone"]),
            ("License", doctor["license_email"]),
            ("Specialization", doctor["specialization"]),
            ("Experience", f'{doctor["experience"]} years'),
            ("Clinic", doctor["clinic"]),
            ("Location", doctor["location"]),
            ("Services", doctor["services"]),
            ("Status", doctor["status"].upper()),
            ("Employee ID", doctor.get("employee_id") or "-"),
        ]

        for label, value in fields:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(60, y, f"{label}:")
            c.setFont("Helvetica", 11)
            c.drawString(180, y, str(value))
            y -= 18

        # AGREEMENT
        y -= 20
        c.setFillColor(colors.HexColor("#0f4c81"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Doctor Declaration Agreement")

        y -= 20
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)

        agreement_lines = [
            "• I confirm that all information provided is true, accurate, and complete.",
            "• My education and qualifications are completed in India and valid.",
            "• I understand registration will undergo verification.",
            "• False or forged information may lead to removal.",
            "• I consent to internal verification and policy compliance."
        ]

        for line in agreement_lines:
            c.drawString(60, y, line)
            y -= 14

        # SIGNATURE
        c.setFillColor(colors.HexColor("#e8f5e9"))
        c.roundRect(40, 80, width - 80, 70, 10, fill=True, stroke=False)

        c.setFillColor(colors.HexColor("#2e7d32"))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, 120, "✔ Verified by HealthyLife Admin")

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(60, 105, "Digitally Signed & Approved")

        # FOOTER
        c.setFillColor(colors.grey)
        c.setFont("Helvetica", 8)
        c.drawString(50, 50, "This is a system generated verification document.")
        c.drawString(60, 60, "Authorized By Mahboob Attar")

        c.save()

        logger.info(f"PDF generated at {pdf_path}")

        return pdf_path
