import json
import os
import time
import requests as req
from flask import (
    Blueprint,
    abort,
    flash,
    request,
    redirect,
    render_template,
    url_for,
    session,
)
from app.site.models.user_login_model import UserLogin
from app.site.forms.form_auth import FormLogin
from ..lib.base_url import base_url
from flask_login import login_user, current_user, login_required, logout_user
from urllib.parse import urljoin, urlparse
from ..lib.json import JsonFileObject

login = Blueprint("login", __name__, url_prefix="/", template_folder="../templates/")

JSON_FILE = os.getcwd() + "/data.json"


def write_json(data, filename=JSON_FILE):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@login.get("/")
def index():
    return redirect(url_for("login.masuk"))


# def index():
#     form = FormLogin(request.form)
#     if session['is_au']thenticated:
#         if session['group'] == "admin":
#             return redirect(url_for("admin2.index"))
#         if session['group'] == "guru":
#             return redirect(url_for("guru2.index"))
#     # next = get_redirect_target()
#     session["next"] = request.args.get("next")
#     return render_template("auth/login.html", form=form)


@login.route("sign-in", methods=["GET", "POST"])
def masuk():
    if current_user.is_authenticated:
        if current_user.group == "admin":
            return redirect(url_for("admin2.index"))
        elif current_user.group == "guru":
            return redirect(url_for("guru2.index"))

    url = base_url + "api/v2/auth/login"
    form = FormLogin(request.form)
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        group = request.form.get("level")
        remember = form.remember.data

        payload = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        resp = req.post(url=url, data=payload, headers=headers)
        jsonResp = resp.json()
        t = JsonFileObject(JSON_FILE)
        t.write_json(data=jsonResp)
        session.update(jsonResp)
        if resp.status_code == 200:
            user = UserLogin()
            user.id = session.get("id")
            # user.group = session.get("group")
            login_user(user, remember=remember)
            if "next" in session and session["next"]:
                if is_safe_url(session["next"]):
                    return redirect(session["next"])

            if current_user.group == "admin" and group == "admin":
                flash(
                    f"Login berhasil. Selamat datang {str(jsonResp['group']).upper()}. Status : {resp.status_code}",
                    "success",
                )
                time.sleep(1.5)
                return redirect(url_for("admin2.index"))
            elif current_user.group == "guru" and group == "guru":
                flash(
                    f"Login berhasil. Selamat datang {str(jsonResp['group']).upper()}. Status : {resp.status_code}",
                    "success",
                )
                time.sleep(1.5)
                return redirect(url_for("guru2.index"))
            else:
                logout_user()
                flash(
                    f"Login gagal. anda salah memilih level pengguna. silahkan pilih level pengguna yang sesuai.",
                    "error",
                )
        else:
            flash(f'{jsonResp["msg"]} Status Code : {resp.status_code}', "error")
            # return render_template("auth/login.html", form=form)
    session["next"] = request.args.get("next")
    return render_template("auth/login.html", form=form)


#         if "next" in session and session["next"]:
#             if is_safe_url(session["next"]):
#                 return redirect(session["next"])
#         if session['group'] == "admin" and group == "admin":
#             flash(
#                 f"Login berhasil. Selamat datang {str(jsonResp['group']).upper()}. Status : {resp.status_code}",
#                 "success",
#             )
#             return redirect(url_for("admin2.index"))
#             # return redirect_back("admin2.index")
#         elif session['group'] == "guru" and group == "guru":
#             flash(
#                 f"Login berhasil. Selamat datang {str(jsonResp['group']).upper()}. Status : {resp.status_code}",
#                 "success",
#             )
#             return redirect(url_for("guru2.index"))
#             # return redirect_back("guru2.index")

#     else:
#         flash(f"{jsonResp['msg']} Status : {resp.status_code}", "error")
# session["next"] = request.args.get("next")
# return render_template("auth/login.html", form=form)


@login.route("sign-out")
@login_required
def logout():
    session.clear()
    logout_user()
    t = JsonFileObject(JSON_FILE)
    t.clear_json()
    return redirect(url_for("login.index"))
