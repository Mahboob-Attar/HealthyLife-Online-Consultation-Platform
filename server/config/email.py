import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASS = os.getenv("SMTP_PASS")


#  Send Plain Text Email
def send_email(to, subject, body):
    try:
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = to

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASS)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print("Email Error:", e)
        return False


#  Send HTML Email (WITH ATTACHMENTS SUPPORT)
def send_email_html(to, subject, html, attachments=None):
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = to

        # attach html body
        msg.attach(MIMEText(html, "html"))

        # attach files if provided
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASS)
            smtp.send_message(msg)

        return True

    except Exception as e:
        print("HTML Email Error:", e)
        return False
