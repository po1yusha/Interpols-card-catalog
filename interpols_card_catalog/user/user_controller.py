from flask import Flask, redirect
from flask import request
from flask import render_template
from user.user_service import UserService, ExistUserException
from user.user_repository import UserEntity
from session_filter import get_session


def init(app: Flask, user_service: UserService):
    @app.route("/users")
    def users_list_page():
        user_list = user_service.get_all_users()
        session = get_session(request)
        user = user_service.get_user_by_login(session["login"])
        return render_template("users_list_page.html", user_list=user_list,
                               message=request.args.get("message", ""),
                               user_name=user.name)

    @app.route("/api/users/delete")
    def delete():
        deleted_login = request.args["login"]
        session = get_session(request)

        if deleted_login == session["login"]:
            return redirect("/users?message=Cannot remove your account")

        user_service.delete_user(deleted_login)

        return redirect("/users")

    @app.route("/users/create")
    def new_user_page():
        return render_template("new_user_page.html",
                               message=request.args.get("message", ""),
                               login=request.args.get("login", ""),
                               name=request.args.get("name", ""))

    def validate_create_user_form(form, required_fields: [str]):
        error_message = "Please complete fields:"
        error = False

        for field in required_fields:
            value = form.get(field)
            if value == '':
                error_message += " " + field
                error = True

        if error:
            return error_message
        else:
            return None

    @app.route("/api/users/new", methods=["POST"])
    def create():
        error_message = validate_create_user_form(request.form, ["name", "login", "password"])

        if error_message is not None:
            return redirect("/users/create?message=" + error_message
                            + "&login=" + request.form.get("login", "")
                            + "&name=" + request.form.get("name", ""))

        new_user_login = request.form.get("login")
        user = UserEntity(request.form.get("login"), request.form.get("password"), request.form.get("name"))

        try:
            user_service.add_user(new_user_login, user)
        except ExistUserException:
            return redirect("/users/create?message=Entered login already exists")
        return redirect("/users")
