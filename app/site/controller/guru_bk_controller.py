from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    make_response,
    url_for,
)
from flask_login import login_required, current_user
from app.models.master_model import GuruBKModel
from app.models.data_model import *
from app.site.forms.form_guru_bk import FormTambahPelanggar

guru_bk = Blueprint(
    "guru_bk",
    __name__,
    static_folder="../static/",
    template_folder="../templates/",
    url_prefix="/guru-bk/",
)


def get_guru_bk():
    sql = GuruBKModel.query.filter_by(guru_id=current_user.id).first()
    return sql


@guru_bk.route("index")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            response = make_response(
                render_template("guru_bk/index_bk.html", guru_bk=get_guru_bk())
            )
            return response
        else:
            return abort(404)


@guru_bk.route("data-pelanggar", methods=["GET", "POST"])
@login_required
def data_pelanggar():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            response = make_response(
                render_template(
                    "guru_bk/modul/pelanggaran/daftar-pelanggar.html",
                    guru_bk=get_guru_bk(),
                )
            )
            return response
        else:
            return abort(404)


@guru_bk.route("data-pelanggar/add", methods=["GET", "POST"])
@login_required
def add_data_pelanggar():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormTambahPelanggar()
            sql_kelas = KelasModel.query.all()
            sql_jenis = JenisPelanggaranModel.query.all()
            sql_siswa = SiswaModel.query.all()
            for i in sql_kelas:
                form.kelas.choices.append((i.id, i.kelas))
            for i in sql_jenis:
                form.jenisPelanggaran.choices.append((i.id, i.jenis))

            if request.method == "POST":
                siswa_id = request.form.get("siswa")
                jenis_id = request.form.get("jenisPelanggaran")
                pelapor = request.form.get("pelapor")

                insert_pelanggar = PelanggaranModel(
                    siswaId=siswa_id, jenisPelanggaranId=jenis_id, pelapor=pelapor
                )
                db.session.add(insert_pelanggar)
                db.session.commit()
                response = make_response(redirect(url_for("guru_bk.data_pelanggar")))
                flash(f"Data Pelanggar Berhasil Di Tambahkan.", "success")
                return response
            else:
                response = make_response(
                    render_template(
                        "guru_bk/modul/pelanggaran/tambah-pelanggar.html",
                        guru_bk=get_guru_bk(),
                        form=form,
                        sql_siswa=sql_siswa,
                    )
                )
                return response
        else:
            return abort(404)
