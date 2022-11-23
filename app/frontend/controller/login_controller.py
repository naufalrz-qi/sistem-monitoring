import json
import requests as req
from flask import Blueprint, request, redirect, render_template, url_for, session
from app.frontend.models.user_login_model import UserLogin
from app.frontend.forms.form_auth import FormLogin
from ..lib.base_url import base_url
from flask_login import login_user, current_user

login = Blueprint("login", __name__, url_prefix="/", template_folder="../templates/")


@login.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("admin2.index"))
    form = FormLogin(request.form)
    return render_template("auth/login.html", form=form)


@login.route("sign-in", methods=["GET", "POST"])
def masuk():
    url = base_url + "api/v2/auth/login"
    form = FormLogin(request.form)
    if request.method == "POST" and form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        group = request.form.get("level")

        payload = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        resp = req.post(url=url, data=payload, headers=headers)
        jsonResp = resp.json()
        # user = UserLogin(id=jsonResp["id"], firstName=jsonResp["first_name"])
        users = UserLogin()
        users.id = jsonResp["id"]
        login_user(users)
        session["username"] = jsonResp["username"]
        session["group"] = jsonResp["group"]
        session["firstName"] = jsonResp["first_name"]
        session["lastName"] = jsonResp["last_name"]
        session["gender"] = jsonResp["gender"]
        session["alamat"] = jsonResp["alamat"]

        if jsonResp["group"] == "siswa":
            return "Halaman Siswa"
        elif jsonResp["group"] == group:
            return redirect(url_for("admin2.index"))
        else:
            return redirect(url_for("login.index"))
    return render_template("auth/login.html", form=form)
