import random
from datetime import datetime, timedelta
from server.config.db import get_connection
from server.config.email import send_email, render_email_template


def generate_otp():
    """Generate a 6-digit random OTP"""
    return str(random.randint(100000, 999999))


def store_otp_and_send_email(email, purpose="signup"):
    otp = generate_otp()
    expires = datetime.now() + timedelta(minutes=2)

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Delete expired or used OTPs for safety
        cur.execute("DELETE FROM otp_verification WHERE expires_at < NOW() OR used = 1")

        # Insert fresh OTP
        cur.execute("""
            INSERT INTO otp_verification (email, otp, purpose, expires_at, used)
            VALUES (%s, %s, %s, %s, 0)
        """, (email, otp, purpose, expires))

        conn.commit()
        cur.close()
        conn.close()

        # Build email HTML from template
        html = render_email_template(
            "otp_email.html",
            otp=otp,
            validity="2 minutes"
        )

        # Fallback text message
        text = f"Your HealthyLife OTP is {otp}. Valid for 2 minutes."

        send_email(
            to=email,
            subject="HealthyLife Verification OTP",
            html_content=html,
            text_content=text
        )

        return True, "OTP sent successfully"

    except Exception as e:
        print("OTP Error:", e)
        return False, "Failed to send OTP"
