from datetime import datetime, timedelta
import random
import threading
from flask import render_template
from server.config.db import get_connection
from server.config.email import send_email_html


def generate_otp():
    return str(random.randint(100000, 999999))


def send_email_background(email, subject, html_body):
    try:
        send_email_html(email, subject, html_body)
    except Exception as e:
        print("Email sending failed:", e)


def create_and_send_otp(email, purpose="signup"):
    try:
        otp = generate_otp()
        expires = datetime.now() + timedelta(minutes=2)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW() OR used = 1")

        cur.execute("""
            INSERT INTO otp_verification (email, otp, purpose, expires_at, used)
            VALUES (%s, %s, %s, %s, 0)
        """, (email, otp, purpose, expires))

        conn.commit()
        cur.close()
        conn.close()

        # Select template
        if purpose == "reset":
            template = "emails/resetotp_email.html"
            subject = "HealthyLife Password Reset OTP"
        else:
            template = "emails/otp_email.html"
            subject = "HealthyLife Verification OTP"

        html_body = render_template(template, otp=otp)

        #  SEND EMAIL IN BACKGROUND THREAD
        threading.Thread(
            target=send_email_background,
            args=(email, subject, html_body),
            daemon=True
        ).start()

        return {"status": "success", "msg": "OTP is being sent"}

    except Exception as e:
        return {"status": "error", "msg": f"Failed to generate OTP: {str(e)}"}



def verify_otp(email, otp, purpose="signup"):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Remove expired OTPs
    cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW()")

    cur.execute("""
        SELECT * FROM otp_verification
        WHERE email=%s AND otp=%s AND purpose=%s AND used=0
        ORDER BY id DESC LIMIT 1
    """, (email, otp, purpose))

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return {"status": "error", "msg": "Invalid or expired OTP"}

    # Mark as used
    cur.execute("UPDATE otp_verification SET used=1 WHERE id=%s", (row['id'],))
    conn.commit()

    cur.close()
    conn.close()

    return {"status": "success", "msg": "OTP verified"} 