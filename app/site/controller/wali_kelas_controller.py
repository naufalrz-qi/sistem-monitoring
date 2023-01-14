from flask import (
    Flask,
    make_response,
    url_for,
    request,
    redirect,
    flash,
    render_template,
    Blueprint,
)
from flask_login import current_user, login_required
from sqlalchemy import func
from app.models.data_model import AbsensiModel
from app.models.master_model import NamaBulanModel, WaliKelasModel
from app.models.user_details_model import SiswaModel
from app.site.forms.form_letter_report import FormRekapAbsenWali
from ...extensions import db

wali_kelas = Blueprint(
    "wali_kelas",
    __name__,
    static_folder="../static/",
    url_prefix="/wali-kelas/",
    template_folder="../templates/",
)

query = lambda sql: sql


def sql_wali_():
    sql = query(
        sql=db.session.query(WaliKelasModel)
        .filter(WaliKelasModel.guru_id == current_user.id)
        .first()
    )
    return sql


@wali_kelas.route("/index")
@login_required
def index():
    return render_template("wali_kelas/index_wali_kelas.html", sql_wali_=sql_wali_())


@wali_kelas.route("data-siswa")
@login_required
def data_siswa():
    sql_siswa = (
        db.session.query(SiswaModel)
        .filter(SiswaModel.kelas_id == sql_wali_().kelas_id)
        .all()
    )

    response = make_response(
        render_template(
            "wali_kelas/modul/siswa/data_siswa.html",
            sql_siswa=sql_siswa,
            sql_wali_=sql_wali_(),
        )
    )
    return response


@wali_kelas.route("rekap-absen")
@login_required
def rekap_absen():
    form = FormRekapAbsenWali()
    sql_bulan = NamaBulanModel.query.all()
    sql_tahun = AbsensiModel.query.group_by(func.year(AbsensiModel.tgl_absen)).all()

    for i in sql_bulan:
        form.bulan.choices.append((i.id, i.nama_bulan.upper()))

    for i in sql_tahun:
        form.tahun.choices.append((i.tgl_absen.year, i.tgl_absen.year))

    response = make_response(
        render_template(
            "wali_kelas/modul/rekap_kehadiran/rekap_by_kelas.html",
            form=form,
            sql_wali_=sql_wali_(),
        )
    )

    return response
