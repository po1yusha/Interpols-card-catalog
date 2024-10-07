from flask import Flask, redirect
from flask import request
import uuid

session_storage = {}


def is_session_exist(request):
    if not request.cookies:
        return False
    if not request.cookies.get("session"):
        return False
    return True


def get_session(request) -> dict:
    if not is_session_exist(request):
        return None
    session_id = request.cookies.get("session")
    if session_id not in session_storage:
        session_storage[session_id] = {}
    return session_storage[session_id]


def init(app: Flask):
    @app.after_request
    def set_cookies_if_not_exist(response):
        if not is_session_exist(request):
            response.set_cookie("session", str(uuid.uuid4()))
        return response
