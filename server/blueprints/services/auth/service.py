from flask import jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from server.config.db import get_connection
from server.config.email import send_email_html
from datetime import datetime
from .otp_service import verify_otp as verify_otp_service


# SIGNUP (USER ONLY
def auth_signup(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"status": "error", "msg": "All fields required"}), 400

    email = email.strip().lower()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Check if email already exists
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"status": "error", "msg": "Email already registered"}), 400

    hashed_pass = generate_password_hash(password)

    # Insert normal user (not admin)
    cur.execute("""
        INSERT INTO users (name, email, password_hash, is_admin,email_verified)
        VALUES (%s, %s, %s, 0,1)
    """, (name, email, hashed_pass,))

    conn.commit()
    cur.close()
    conn.close()

    # Send account created email
    html = render_template(
        "emails/accountcreated_email.html",
        user_name=name,
        year=datetime.now().year
    )

    send_email_html(email, "Welcome to HealthyLife", html)

    return jsonify({
        "status": "success",
        "msg": "Account created successfully"
    }), 200

# LOGIN (USER / ADMIN)
def auth_login(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "msg": "Email & password required"}), 400

    email = email.strip().lower()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return jsonify({"status": "error", "msg": "User not found"}), 404

    if not check_password_hash(user["password_hash"], password):
        cur.close()
        conn.close()
        return jsonify({"status": "error", "msg": "Incorrect password"}), 400

    cur.close()
    conn.close()

    #  FIXED ROLE SYSTEM
    session.clear()
    session["logged_in"] = True
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    if user["is_admin"] == 1:
        session["role"] = "admin"
    else:
        session["role"] = "user"

    return jsonify({
        "status": "success",
        "msg": "Login successful",
        "name": user["name"],
        "role": session["role"]
    }), 200

def reset_password(data):
    email = data.get("email")
    password = data.get("password")
    otp = data.get("otp")

    if not email or not password or not otp:
        return jsonify({
            "status": "error",
            "msg": "Email, OTP & new password required"
        }), 400

    email = email.strip().lower()

    if len(password) < 6:
        return jsonify({
            "status": "error",
            "msg": "Password must be at least 6 characters"
        }), 400

    # VERIFY OTP FOR RESET PURPOSE
    otp_result = verify_otp_service(email, otp, purpose="reset")

    if otp_result["status"] != "success":
        return jsonify(otp_result), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({
            "status": "error",
            "msg": "Email not found"
        }), 404

    hashed_pass = generate_password_hash(password)

    cur.execute(
        "UPDATE users SET password_hash=%s WHERE email=%s",
        (hashed_pass, email)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "status": "success",
        "msg": "Password reset successful"
    }), 200