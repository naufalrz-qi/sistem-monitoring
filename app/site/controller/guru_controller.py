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
import asyncio
from flask_login import current_user, login_required
from sqlalchemy import and_, func
from app.site.forms.form_absen import AbsensiForm
from ...backend.extensions import db
from app.backend.lib.base_model import BaseModel
from app.backend.models.user_details_model import GuruModel, SiswaModel
from app.site.forms.form_guru import FormGetProfileGuru, FormUpdatePassword
from ..models.user_login_model import *
from ...backend.models.master_model import (
    KelasModel,
    MengajarModel,
    HariModel,
    SemesterModel,
    WaliKelasModel,
)
from ...backend.lib.date_time import format_indo, tomorrow_, today_
from werkzeug.security import generate_password_hash, check_password_hash
from ...backend.models.data_model import AbsensiModel
from datetime import datetime
from sqlalchemy import exists


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
    sql = day(
        sql=(
            db.session.query(MengajarModel)
            .join(HariModel)
            .join(SemesterModel)
            .filter(MengajarModel.guru_id == current_user.id)
            .filter(MengajarModel.hari_id == HariModel.id)
            .filter(HariModel.hari == today_())
            .filter(SemesterModel.is_active == 1)
            .all()
        )
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
                    .join(SemesterModel)
                    .filter(MengajarModel.guru_id == current_user.id)
                    .filter(MengajarModel.hari_id == HariModel.id)
                    .filter(HariModel.hari == today_())
                    .filter(SemesterModel.is_active == "1")
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
    if current_user.group == "guru":
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
    else:
        abort(404)


@guru2.route("/profile/<int:id>", methods=["GET", "POST"])
@login_required
def update_profile(id):
    if current_user.group == "guru":
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
    else:
        return abort(404)


@guru2.route("update-password", methods=["POST", "GET", "PUT"])
@login_required
def update_pswd():
    if current_user.group == "guru":
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
    else:
        return abort(404)


@guru2.route("jadwal-mengajar")
@login_required
def jadwal_mengajar():
    if current_user.group == "guru":
        base = BaseModel(MengajarModel)
        mengajar = base.get_all_filter_by(
            base.model.hari_id.asc(), guru_id=current_user.id
        )
        sql_mengajar = (
            db.session.query(MengajarModel)
            .join(SemesterModel)
            .filter(SemesterModel.is_active == 1)
            .filter(MengajarModel.guru_id == current_user.id)
            .order_by(MengajarModel.hari_id.asc())
            .order_by(MengajarModel.jam_mulai.asc())
            .all()
        )
        """GET WITH GENERAL FUNCTION"""
        # sqlToday = get_kelas_today()
        # sqlTomorrow = get_kelas_tomorrow()

        """GET WITH LAMBDA FUNCTION"""
        sqlToday = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == today_())
                .filter(SemesterModel.is_active == 1)
                .all()
            )
        )
        sqlTomorrow = day(
            sql=(
                db.session.query(MengajarModel)
                .join(HariModel)
                .join(SemesterModel)
                .filter(MengajarModel.guru_id == current_user.id)
                .filter(MengajarModel.hari_id == HariModel.id)
                .filter(HariModel.hari == tomorrow_())
                .filter(SemesterModel.is_active == 1)
                .all()
            )
        )

        return render_template(
            "guru/modul/jadwal_mengajar/jadwal_mengajar.html",
            # sqlJadwal=mengajar,
            sqlJadwal=sql_mengajar,
            sqlToday=sqlToday,
            sqlTomorrow=sqlTomorrow,
        )
    else:
        return abort(404)


@guru2.route("/absensi-pelajaran/<int:mengajar_id>", methods=["GET", "POST"])
@login_required
def absensi(mengajar_id):
    if current_user.group == "guru":
        form = AbsensiForm()
        """
            mengambil smua data pada tabel master mengajar dengan filter by mengajar id
            sebagai parameter, dan menyimpan data mengajar pada dictionary data mengajar
        """
        base_mengajar = BaseModel(MengajarModel)
        mengajar = base_mengajar.get_all_filter_by(id=mengajar_id)

        data_mengajar = {}
        for i in mengajar:
            data_mengajar["kelas_id"] = i.kelas_id
            data_mengajar["kelas"] = i.kelas.kelas
            data_mengajar["mengajar_id"] = i.id
            data_mengajar["mapel"] = i.mapel.mapel
        """
            mengambil semua data siswa dengan filter kelas id pada tabel siswa
            dan di join dengan kelas id pada tabel master mengajar. Dan data
        """
        base_siswa = BaseModel(SiswaModel)
        # siswa = base_siswa.get_all_filter_by(kelas_id=data_mengajar["kelas_id"])
        siswa = (
            db.session.query(SiswaModel)
            # .join(AbsensiModel)
            # .filter(AbsensiModel.tgl_absen == AbsensiModel.tgl_absen)
            .filter(SiswaModel.kelas_id == data_mengajar["kelas_id"])
            .filter(
                ~exists(AbsensiModel.siswa_id)
                .where(SiswaModel.user_id == AbsensiModel.siswa_id)
                .where(AbsensiModel.tgl_absen == datetime.date(datetime.today()))
                .where(AbsensiModel.mengajar_id == mengajar_id)
            )
            .all()
        )
        """
            mengambil semua id dan nama kelas pada tabel kelas melalui tabel siswa
            yang sudah di relasikan dengan tabel kelas, lalu di simpan dalam
            variabel dictionoary data.
        """
        data = {}
        for i in siswa:
            data["kelas_id"] = i.kelas_id
            data["kelas"] = i.kelas.kelas

        """
            Mengambil semua data pada Tabel Mengajar
            dengan filter berdasarkan hari dan guru id
        """
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
        date = datetime.date(datetime.today())

        """
        Menghitung jumlah pertemuan dengan filter berdasarkan tabel MENGAJAR ID
        """
        sqlCountPertemuan = day(
            sql=db.session.query(AbsensiModel)
            .filter(AbsensiModel.mengajar_id == data_mengajar["mengajar_id"])
            .order_by(AbsensiModel.pertemuan_ke.desc())
            .limit(1)
            .count()
        )

        """
            MENAMBIL DATA ABSEN PERHARI DENGAN FILTER BERDASARKAN TANGGAL PERHARI
            UNTUK FILTER PERTEMUAN-KE N JIKA TANGGALNYA MASIH SAMA ATAU DI HARI YANG
            SAMA PADA ABSEN MAKA PERTEMUAN KE TIDAK AKAN BERUBAH
        """
        sqlTglAbsen = day(
            sql=db.session.query(AbsensiModel)
            .join(SiswaModel)
            .filter(AbsensiModel.tgl_absen == date)
            .filter(AbsensiModel.siswa_id == SiswaModel.user_id)
            .order_by(AbsensiModel.pertemuan_ke.desc())
            .first()
        )

        """
            MENGHITUNG PERTEMUAN SETIAP SUDAH MELAKUKAN ABSEN, DAN HASIL
            KALKULASI DARI PERTEMUAN AKAN TER-TAMBAH SECARA OTOMATIS
            ZDI PERTEMUAN SELANJUTNYA
        """
        if sqlCountPertemuan != 0:
            data["pertemuan"] = (
                sqlCountPertemuan + 1 if sqlTglAbsen is None else sqlCountPertemuan
            )

        else:
            data["pertemuan"] = 1
        absen = []

        if request.method == "POST":
            for n in range(1, len(siswa) + 1):
                siswa_id = request.form.get(f"userId-{n}")
                mengajar_id = request.form.get(f"mengajarId")
                tgl_absen = request.form["today"]
                ket = request.form.get(f"ket-{n}")
                pertemuan_ke = request.form["pertemuan"]

                absen.append(ket)
                base_absesn = BaseModel(
                    AbsensiModel(
                        mengajar_id=mengajar_id,
                        siswa_id=siswa_id,
                        tgl_absen=tgl_absen,
                        ket=ket,
                        pertemuan=pertemuan_ke,
                    )
                )

                if None in absen:
                    # flash(
                    #     # f"Ma'af keterangan Kehadiran siswa wajib dipilih secara menyeluruh dengan sesuai keadaan siswa.",
                    #     f"Ma'af.! keterangan Kehadiran siswa wajib dipilih sebelum menyelesaikan absen hari ini.",
                    #     "error",
                    # )
                    pass
                else:
                    sqlPertemuan = day(
                        sql=db.session.query(AbsensiModel)
                        .filter(AbsensiModel.mengajar_id == mengajar_id)
                        .filter(
                            AbsensiModel.tgl_absen == datetime.date(datetime.today())
                        )
                        .filter(AbsensiModel.siswa_id == siswa_id)
                        .count()
                    )
                    if sqlPertemuan > 0:
                        flash(
                            "Ma'af.! Absen kehadiran hari ini telah di input", "error"
                        )
                    else:

                        base_absesn.create()
                        flash(
                            f"Kelas : {data.get('kelas')} telah selesai melaukan absen kehadiran. untuk mengubah kehadiran",
                            "success",
                        )
            return redirect(
                url_for("guru2.absensi", mengajar_id=data_mengajar["mengajar_id"])
            )
        return render_template(
            "guru/modul/absen/absensi.html",
            model=siswa,
            sqlToday=sqlToday,
            data=data,
            form=form,
            today=date,
            data_mengajar=data_mengajar,
        )
    else:
        return abort(404)


@guru2.route("update-absensi/<int:mengajar_id>", methods=["GET", "POST"])
@login_required
def update_absen(mengajar_id):
    if current_user.group == "guru":
        data = {}
        """
        Mengambil semua data pada Tabel Mengajar
        dengan filter berdasarkan hari dan guru id
        """
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

        base_mengjar = BaseModel(MengajarModel)
        sql_mengajar = base_mengjar.get_all_filter_by(id=mengajar_id)
        for i in sql_mengajar:
            data["mengajar_id"] = i.id
            data["kelas_id"] = i.kelas_id
            data["kelas"] = i.kelas.kelas
            data["mapel"] = i.mapel.mapel

        base_siswa = BaseModel(SiswaModel)
        sql_siswa = base_siswa.get_all_filter_by(kelas_id=data["kelas_id"])

        base_absensi = BaseModel(AbsensiModel)
        sql_absensi = base_absensi.get_all_filter_by(mengajar_id=mengajar_id)

        if request.method == "POST":

            for i in range(1, len(sql_absensi) + 1):
                ket = request.form.get(f"ket-{i}")
                siswa_id = request.form.get(f"siswaID-{i}")

                sql_update_absen = (
                    db.session.query(AbsensiModel)
                    .filter(AbsensiModel.mengajar_id == mengajar_id)
                    .filter(AbsensiModel.siswa_id == siswa_id)
                    .scalar()
                )

                sql_update_absen.ket = ket

                db.session.commit()

            flash(f"Anda telah melakukan perubahan absensi siswa.", "info")

            return redirect(url_for("guru2.absensi", mengajar_id=mengajar_id))

        return render_template(
            "guru/modul/absen/update_absensi.html",
            sqlToday=sqlToday,
            sql_absensi=sql_absensi,
            data=data,
            sql_siswa=sql_siswa,
        )
    else:
        return abort(404)


@guru2.route("/daftar-hadir", methods=["GET", "POST"])
@login_required
async def daftar_kehadiran():

    return render_template("guru/modul/absen/daftar_hadir.html")
