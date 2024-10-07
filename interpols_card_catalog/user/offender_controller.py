from flask import Flask, redirect
from flask import request
from flask import render_template
from user.offender_service import LastOffenderException, ExistOffenderException, OffenderService
from user.bio_offender_repository import BioCrimeEntity
from user.user_service import UserService
from session_filter import get_session
import json
import uuid


def init(app: Flask, offender_service: OffenderService, user_service: UserService):
    @app.route("/offenders")
    def offender_list_page():
        session = get_session(request)
        user = user_service.get_user_by_login(session["login"])
        offender_list = offender_service.get_offenders_with_filter(request.args)

        return render_template("crime_list_page.html", offender_list=offender_list, user_name=user.name)

    def validate_create_offender_form(form, required_fields: [str]):
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

    @app.route("/api/offenders/new", methods=["POST"])
    def create():
        form = json.loads(request.data)
        form["id"] = str(uuid.uuid4())

        error_message = validate_create_offender_form(form, ["second_name", "name",
                                                             "sex", "date_of_birth",
                                                             "criminal_profession"])

        if error_message is not None:
            return json.dumps({
                'error': error_message
            })

        new_offender_id = form.get("id")
        offender = BioCrimeEntity(form.get("id"), form.get("second_name", ""), form.get("name", ""),
                                  form.get("sex", ""),
                                  form.get("alias", ""),
                                  form.get("height", ""),
                                  form.get("hair_color", ""),
                                  form.get("eye_color", ""),
                                  form.get("special_features", ""),
                                  form.get("citizenship", ""),
                                  form.get("residence", ""),
                                  form.get("language", ""),
                                  form.get("place_of_birth", ""),
                                  form.get("date_of_birth", ""),
                                  form.get("criminal_profession", ""),
                                  form.get("last_crime", ""),
                                  form.get("status", "0"),
                                  form.get("group_criminal", ""))

        try:
            offender_service.add_offender(new_offender_id, offender)
        except ExistOffenderException:
            return json.dumps({
                'error': "Offender already exist"
            })
        return json.dumps({})

    @app.route("/api/offenders/edit", methods=["POST"])
    def edit():
        offender_id = request.args["id"]
        form = json.loads(request.data)

        error_message = validate_create_offender_form(form, ["second_name", "name",
                                                             "sex", "date_of_birth",
                                                             "criminal_profession"])

        if error_message is not None:
            return json.dumps({
                'error': error_message
            })

        offender = BioCrimeEntity(offender_id, form.get("second_name", ""), form.get("name", ""),
                                  form.get("sex", ""),
                                  form.get("alias", ""),
                                  form.get("height", ""),
                                  form.get("hair_color", ""),
                                  form.get("eye_color", ""),
                                  form.get("special_features", ""),
                                  form.get("citizenship", ""),
                                  form.get("residence", ""),
                                  form.get("language", ""),
                                  form.get("place_of_birth", ""),
                                  form.get("date_of_birth", ""),
                                  form.get("criminal_profession", ""),
                                  form.get("last_crime", ""),
                                  form.get("status", "0"),
                                  form.get("group_criminal", ""))

        try:
            offender_service.edit_offender(offender_id, offender)
        except ExistOffenderException:
            return json.dumps({
                'error': "Offender already exist"
            })
        return json.dumps({})

    @app.route("/api/offenders/delete")
    def delete():
        deleted_id = request.args["id"]
        try:
            offender_service.delete_offender(deleted_id)
        except LastOffenderException:
            return json.dumps({
                'error': "Cannot remove last offender"
            })
        return redirect("/offenders")

    @app.route("/api/offenders/archive")
    def arcive():
        archived_id = request.args["id"]
        offender_service.archive_offender(archived_id)
        return redirect("/offenders")

    @app.route("/api/offenders/personal")
    def show_personal_info():
        personal_id = request.args["id"]
        personal_offender = offender_service.get_offender_by_id(personal_id)
        return render_template("personal_crime_page.html", personal_offender=personal_offender)

    @app.route("/offenders/archive")
    def archive_offender_list_page():
        archive_offender_list = offender_service.get_all_archive_offenders()
        return render_template("archive_offenders_page.html", archive_offender_list=archive_offender_list)

    @app.route("/offenders/group")
    def group_offender_list_page():
        criminal_group = request.args["group_criminal"]
        criminal_group_list = offender_service.get_group_offenders(criminal_group)
        return render_template("criminal_group_page.html", criminal_group_list=criminal_group_list)
