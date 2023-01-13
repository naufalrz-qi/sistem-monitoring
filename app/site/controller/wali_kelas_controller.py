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
from app.models.master_model import WaliKelasModel
from app.models.user_details_model import SiswaModel
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
