from flask import (
    abort,
    request,
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
    render_template,
    escape,
)
from flask_login import current_user, login_required
from app.frontend.forms.form_absen import AbsensiForm
from ...backend.extensions import db
from app.backend.lib.base_model import BaseModel
from app.backend.models.user_details_model import GuruModel, SiswaModel
from app.frontend.forms.form_guru import FormGetProfileGuru, FormUpdatePassword
from ..models.user_login_model import *
from ...backend.models.master_model import (
    KelasModel,
    MengajarModel,
    HariModel,
    WaliKelasModel,
)
from ...backend.lib.date_time import format_indo, tomorrow_, today_
from werkzeug.security import generate_password_hash, check_password_hash
from ...backend.models.data_model import AbsensiModel
from datetime import datetime

guru2 = Blueprint(
    "guru2",
    __name__,
    url_prefix="/guru-site",
    static_folder="../static/",
    template_folder="../templates/",
)

day = lambda sql: sql
query = lambda sql: sql


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


def check_wali():
    sql = query(
        sql=db.session.query(WaliKelasModel)
        .filter(WaliKelasModel.guru_id == current_user.id)
        .first()
    )
    return sql


@guru2.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.group == "guru":
            """With general function"""
            # sqlToday = get_kelas_today()

            """get With Lambda function"""
            sqlToday = day(
                sql=(
                    db.session.query(MengajarModel)
                    .join(HariModel)
                    .filter(MengajarModel.guru_id == current_user.id)
                    .filter(MengajarModel.hari_id == HariModel.id)
                    .filter(HariModel.hari == today_())
                    .all()
                )
            )
            baseJadwal = BaseModel(MengajarModel)
            mengajar = baseJadwal.get_all_filter_by(
                baseJadwal.model.hari_id.asc(), guru_id=current_user.id
            )
            wali_kelas = check_wali()

            return render_template(
                "guru/index_guru.html",
                sqlJadwal=mengajar,
                sqlToday=sqlToday,
                wali_kelas=wali_kelas,
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
        "guru/modul/akun/profile_guru.html",
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


@guru2.route("update-password", methods=["POST", "GET", "PUT"])
@login_required
def update_pswd():
    base = BaseModel(GuruModel)
    guru = base.get_one(user_id=current_user.id)
    form = FormUpdatePassword()
    if form.validate_on_submit() and request.method == "POST":
        password = request.form.get("password")
        check_pswd = check_password_hash(guru.user.password, password)
        if check_pswd:
            flash(
                f"Pastikan password baru anda tidak boleh sama dengan password sebelumnya.!",
                "error",
            )
        else:
            pswd_hash = generate_password_hash(password)
            guru.user.password = pswd_hash
            base.edit()
            flash(f"Password akun anda telah berhasil di perbaharui.!", "info")

            return redirect(url_for("guru2.index"))
    return render_template("guru/modul/akun/update_password.html", form=form)


@guru2.route("jadwal-mengajar")
@login_required
def jadwal_mengajar():
    base = BaseModel(MengajarModel)
    mengajar = base.get_all_filter_by(base.model.hari_id.asc(), guru_id=current_user.id)
    """GET WITH GENERAL FUNCTION"""
    # sqlToday = get_kelas_today()
    # sqlTomorrow = get_kelas_tomorrow()

    """GET WITH LAMBDA FUNCTION"""
    sqlToday = day(
        sql=(
            db.session.query(MengajarModel)
            .join(HariModel)
            .filter(MengajarModel.guru_id == current_user.id)
            .filter(MengajarModel.hari_id == HariModel.id)
            .filter(HariModel.hari == today_())
            .all()
        )
    )
    sqlTomorrow = day(
        sql=(
            db.session.query(MengajarModel)
            .join(HariModel)
            .filter(MengajarModel.guru_id == current_user.id)
            .filter(MengajarModel.hari_id == HariModel.id)
            .filter(HariModel.hari == tomorrow_())
            .all()
        )
    )
    print(tomorrow_())

    return render_template(
        "guru/modul/jadwal_mengajar/jadwal_mengajar.html",
        sqlJadwal=mengajar,
        sqlToday=sqlToday,
        sqlTomorrow=sqlTomorrow,
    )


@guru2.route("/absensi-pelajaran/<int:kelas_id>", methods=["GET", "POST"])
def absensi(kelas_id):
    form = AbsensiForm()
    base_siswa = BaseModel(SiswaModel)
    siswa = base_siswa.get_all_filter_by(kelas_id=kelas_id)
    sqlToday = day(
        sql=(
            db.session.query(MengajarModel)
            .join(HariModel)
            .filter(MengajarModel.guru_id == current_user.id)
            .filter(MengajarModel.hari_id == HariModel.id)
            .filter(HariModel.hari == today_())
            .all()
        )
    )
    data = {}
    for i in siswa:
        data["kelas_id"] = i.kelas_id
        data["kelas"] = i.kelas.kelas

    for i in sqlToday:
        data["mengajar_id"] = i.id
        data["mapel"] = i.mapel.mapel
    # sqlCountPertemuan = day(
    #     sql=db.session.query(AbsensiModel)
    #     .filter(AbsensiModel.mengajar_id == data["mengajar_id"])
    #     .group_by(AbsensiModel.pertemuan_ke)
    #     .order_by(AbsensiModel.pertemuan_ke.desc())
    #     .limit(1)
    #     .first()
    # )
    date = datetime.date(datetime.today())
    sqlCountPertemuan = day(
        sql=db.session.query(AbsensiModel)
        .filter(AbsensiModel.mengajar_id == data["mengajar_id"])
        .order_by(AbsensiModel.pertemuan_ke.desc())
        .limit(1)
        .count()
        # .filter(AbsensiModel.tgl_absen == date)
    )
    sqlTglAbsen = day(
        sql=db.session.query(AbsensiModel)
        .filter(AbsensiModel.tgl_absen == date)
        .order_by(AbsensiModel.pertemuan_ke.desc())
        .first()
    )

    # print(sqlTglAbsen)
    # print(sqlCountPertemuan.pertemuan_ke)

    if sqlCountPertemuan != 0:
        # data["pertemuan"] = int(sqlCountPertemuan.pertemuan_ke) + 1
        data["pertemuan"] = (
            sqlCountPertemuan + 1 if sqlTglAbsen is None else sqlCountPertemuan
        )

    else:
        data["pertemuan"] = 1

    if request.method == "POST":
        for n in range(1, len(siswa) + 1):
            siswa_id = request.form.get(f"userId-{n}")
            mengajar_id = request.form.get(f"mengajarId")
            tgl_absen = request.form["today"]
            ket = request.form.get(f"ket-{n}")
            pertemuan_ke = request.form["pertemuan"]

            if ket is not None:
                sqlPertemuan = day(
                    sql=db.session.query(AbsensiModel)
                    .filter(AbsensiModel.mengajar_id == mengajar_id)
                    .filter(AbsensiModel.tgl_absen == datetime.date(datetime.today()))
                    .filter(AbsensiModel.siswa_id == siswa_id)
                    .count()
                )
                if sqlPertemuan > 0:
                    flash("Absen hari in telah di input", "error")
                else:
                    base_absesn = BaseModel(
                        AbsensiModel(
                            mengajar_id=mengajar_id,
                            siswa_id=siswa_id,
                            tgl_absen=tgl_absen,
                            ket=ket,
                            pertemuan=pertemuan_ke,
                        )
                    )
                    base_absesn.create()

                    flash(
                        f"Kelas : {data.get('kelas')} telah selesai melaukan absen kehadiran. untuk mengubah kehadiran",
                        "success",
                    )
            else:
                flash(
                    f"Keterangan Kehadiran siswa wajib dipilih secara menyeluruh dengan sesuai keadaan siswa.",
                    "error",
                )
        return redirect(url_for("guru2.absensi", kelas_id=data["kelas_id"]))

    return render_template(
        "guru/modul/absen/absensi.html",
        model=siswa,
        sqlToday=sqlToday,
        data=data,
        form=form,
        today=date,
    )


@guru2.route("/daftar-hadir", methods=["GET", "POST"])
@login_required
def daftar_kehadiran():

    return render_template("guru/modul/absen/daftar_hadir.html")
