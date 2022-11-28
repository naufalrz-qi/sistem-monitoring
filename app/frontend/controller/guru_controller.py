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
from ...backend.extensions import db
from app.backend.lib.base_model import BaseModel
from app.backend.models.user_details_model import GuruModel
from app.frontend.forms.form_guru import FormGetProfileGuru, FormUpdatePassword
from ..models.user_login_model import *
from ...backend.models.master_model import KelasModel, MengajarModel, HariModel
from ...backend.lib.date_time import day_now_indo, tomorrow_, today_
from werkzeug.security import generate_password_hash

guru2 = Blueprint(
    "guru2",
    __name__,
    url_prefix="/guru-site",
    static_folder="../static/",
    template_folder="../templates/",
)


def get_kelas_today():
    sql = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.guru_id == current_user.id)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(HariModel.hari == today_())
        .all()
    )
    return sql


def get_kelas_tomorrow():
    sql = (
        db.session.query(MengajarModel)
        .join(HariModel)
        .filter(MengajarModel.guru_id == current_user.id)
        .filter(MengajarModel.hari_id == HariModel.id)
        .filter(HariModel.hari == tomorrow_())
        .all()
    )
    return sql


@guru2.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.group == "guru":
            sqlToday = get_kelas_today()
            baseJadwal = BaseModel(MengajarModel)
            mengajar = baseJadwal.get_all_filter_by(
                baseJadwal.model.hari_id.asc(), guru_id=current_user.id
            )
            return render_template(
                "guru/index_guru.html",
                sqlJadwal=mengajar,
                sqlToday=sqlToday,
            )
        else:
            abort(404)


@guru2.route("/profile")
@login_required
def profile_guru():
    baseJadwal = BaseModel(MengajarModel)
    mengajar = baseJadwal.get_all_filter_by(
        baseJadwal.model.hari_id.asc(), guru_id=current_user.id
    )
    base = BaseModel(GuruModel)
    guru = base.get_one(user_id=current_user.id)
    form = FormGetProfileGuru()
    form.nip.data = guru.user.username
    form.fullname.data = guru.first_name.title() + " " + guru.last_name.title()
    form.gender.data = guru.gender
    form.agama.data = guru.agama
    form.alamat.data = guru.alamat.title()
    form.telp.data = guru.telp
    sqlToday = get_kelas_today()
    return render_template(
        "guru/modul/profile_guru.html",
        sql=guru,
        form=form,
        sqlJadwal=mengajar,
        sqlToday=sqlToday,
    )


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


@guru2.route("update-password", methods=["GET", "POST"])
# @login_required
def update_password():
    form = FormUpdatePassword()
    base = BaseModel(GuruModel)
    guru = base.get_one(user_id=15)
    if request.method == "GET":
        return render_template("guru/modul/update_password.html", form=form)
    elif request.method == "POST" and form.validate_on_submit():
        password = form.password.data
        pswd_hash = generate_password_hash(password)
        guru.user.password = pswd_hash
        base.edit()
        flash(f"Password akun anda telah berhasil di perbaharui", "info")

        return redirect(url_for("guru2.index"))
    else:
        return render_template("guru/modul/update_password.html", form=form)


@guru2.route("jadwal-mengajar")
@login_required
def jadwal_mengajar():
    base = BaseModel(MengajarModel)
    mengajar = base.get_all_filter_by(base.model.hari_id.asc(), guru_id=current_user.id)
    sqlToday = get_kelas_today()
    sqlTomorrow = get_kelas_tomorrow()
    return render_template(
        "guru/modul/jadwal_mengajar.html",
        sqlJadwal=mengajar,
        sqlToday=sqlToday,
        sqlTomorrow=sqlTomorrow,
    )
