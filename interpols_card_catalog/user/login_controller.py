from flask import Flask, redirect
from flask import request
from flask import render_template
from user.user_service import UserService
from session_filter import get_session


def init(app: Flask, user_service: UserService):
    @app.route("/login")
    def login_page():
        return render_template("interpols_card_catalog.html", massage="Please, enter login and password")

    @app.route('/api/login', methods=["POST"])
    def login_handler():
        login = request.form["login"]
        password = request.form["password"]
        valid = user_service.is_valid_user(login, password)
        session = get_session(request)

        if valid:
            session["login"] = login
            return redirect("/offenders")
        else:
            return render_template("interpols_card_catalog.html", massage="Incorrect password or login")

    @app.route("/api/exit", methods=["POST"])
    def exit_handler():
        session = get_session(request)
        session.clear()
        return redirect("/login")
