from flask import (
    abort,
    request,
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
    render_template,
)
from flask_login import current_user, login_required

from app.backend.lib.base_model import BaseModel
from app.backend.models.user_details_model import GuruModel
from app.frontend.forms.form_guru import FormGetProfileGuru
from ..models.user_login_model import *
from ...backend.models.master_model import MengajarModel

guru2 = Blueprint(
    "guru2",
    __name__,
    url_prefix="/guru-site",
    static_folder="../static/",
    template_folder="../templates/",
)


@guru2.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.group == "guru":
            return render_template("guru/index_guru.html")
        else:
            abort(404)


@guru2.route("/profile")
@login_required
def profile_guru():
    base = BaseModel(GuruModel)
    guru = base.get_one(user_id=current_user.id)
    form = FormGetProfileGuru()
    form.nip.data = guru.user.username
    form.fullname.data = guru.first_name.title() + " " + guru.last_name.title()
    form.gender.data = guru.gender
    form.agama.data = guru.agama
    form.alamat.data = guru.alamat.title()
    form.telp.data = guru.telp
    return render_template("guru/modul/profile_guru.html", sql=guru, form=form)


@guru2.route("/profile/<int:id>", methods=["GET", "POST"])
def update_profile(id):
    base = BaseModel(GuruModel)
    guru = base.get_one(user_id=id)
    form = FormGetProfileGuru(request.form)
    nip = form.nip.data
    fullname = form.fullname.data
    gender = form.gender.data
    agama = form.agama.data
    alamat = form.alamat.data
    telp = form.telp.data
    first_name = ""
    last_name = ""
    first_name, *last_name = fullname.split()
    if len(last_name) == 0:
        last_name = first_name
    elif len(last_name) != 0:
        last_name = " ".join(last_name)
    guru.user.username = nip
    guru.first_name = first_name
    guru.last_name = last_name
    guru.gender = gender
    guru.agama = agama
    guru.alamat = alamat
    guru.telp = telp

    base.edit()
    flash(f"Data profil anda terlah diperbaharui.", "info")
    return redirect(url_for("guru2.profile_guru"))


@guru2.route("jadwal-mengajar")
@login_required
def jadwal_mengajar():
    base = BaseModel(MengajarModel)
    mengajar = base.get_all_filter_by(base.model.hari_id.asc(), guru_id=current_user.id)
    return render_template("guru/modul/jadwal_mengajar.html", sql=mengajar)
