from flask import Flask
from dotenv import load_dotenv
import os
from werkzeug.middleware.proxy_fix import ProxyFix

from server.config.db import get_connection
from server.session.mysql_session import MySQLSessionInterface

load_dotenv()

def create_app():
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static"
    )

    # ================= SECURITY CONFIG =================
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY not set")

    app.config["SESSION_COOKIE_NAME"] = "health_session"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_SECURE", "False") == "True"

    app.config["SESSION_PERMANENT"] = True
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

    # ================= SESSION INTERFACE =================
    app.session_interface = MySQLSessionInterface(
        db_conn_func=get_connection,
        table="sessions"
    )

    # ================= PROXY FIX =================
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # ================= REGISTER BLUEPRINTS =================
    from server.blueprints import init_blueprints
    init_blueprints(app)

    # ================= RUN SQL INIT =================
    with app.app_context():
        from server.config.db_init import init_db
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)