from flask import Flask, redirect
from flask import request
from session_filter import get_session


def init(app: Flask):
    @app.before_request
    def is_autintificated():
        if not (request.full_path.startswith("/static")):
            if not (request.full_path.startswith("/login") or request.full_path.startswith("/api/login")):
                session = get_session(request)
                if session is None:
                    return redirect("/login")
                if session.get("login") is None:
                    return redirect("/login")

