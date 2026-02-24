import uuid
import json
from datetime import datetime, timedelta
from flask.sessions import SessionInterface, SessionMixin


# ================= SESSION OBJECT =================
class MySQLSession(dict, SessionMixin):
    def __init__(self, initial=None, session_id=None):
        super().__init__(initial or {})
        self.session_id = session_id


# ================= SESSION INTERFACE =================
class MySQLSessionInterface(SessionInterface):

    def __init__(self, db_conn_func, table="sessions", lifetime_minutes=15):
        self.db_conn_func = db_conn_func
        self.table = table
        self.lifetime_minutes = lifetime_minutes

    # ================= DELETE EXPIRED SESSIONS =================
    def _delete_expired_sessions(self):
        """Remove all sessions from DB that have expired"""
        conn = self.db_conn_func()
        cur = conn.cursor()
        try:
            cur.execute(
                f"DELETE FROM {self.table} WHERE expiry < %s",
                (datetime.utcnow(),)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

    # ================= OPEN SESSION =================
    def open_session(self, app, request):
        #  Automatically clean expired sessions
        self._delete_expired_sessions()

        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        session_id = request.cookies.get(cookie_name)

        # If no session cookie → create new session
        if not session_id:
            return MySQLSession(session_id=str(uuid.uuid4()))

        conn = self.db_conn_func()
        cur = conn.cursor(dictionary=True)

        try:
            cur.execute(
                f"SELECT data, expiry FROM {self.table} WHERE session_id=%s",
                (session_id,)
            )
            row = cur.fetchone()

            if row and row["expiry"] > datetime.utcnow():
                data = json.loads(row["data"])
                return MySQLSession(data, session_id=session_id)

            # If expired → delete it
            cur.execute(
                f"DELETE FROM {self.table} WHERE session_id=%s",
                (session_id,)
            )
            conn.commit()

        finally:
            cur.close()
            conn.close()

        # Create fresh session
        return MySQLSession(session_id=str(uuid.uuid4()))

    # ================= SAVE SESSION =================
    def save_session(self, app, session, response):
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")

        # If session empty → remove cookie
        if not session:
            response.delete_cookie(cookie_name)
            return

        session_id = session.session_id
        expiry = datetime.utcnow() + timedelta(minutes=self.lifetime_minutes)
        data = json.dumps(dict(session))

        # Clean expired sessions before saving
        self._delete_expired_sessions()

        conn = self.db_conn_func()
        cur = conn.cursor()

        try:
            cur.execute(
                f"""
                REPLACE INTO {self.table} 
                (session_id, data, expiry) 
                VALUES (%s, %s, %s)
                """,
                (session_id, data, expiry)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

        #  Cookie Settings
        response.set_cookie(
            cookie_name,
            session_id,
            expires=expiry,
            httponly=True,
            secure=app.config.get("SESSION_COOKIE_SECURE", False),
            samesite="Lax"
        )