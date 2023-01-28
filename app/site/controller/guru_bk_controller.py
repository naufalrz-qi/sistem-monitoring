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
from app.site.forms.form_guru_bk import FormEditPelanggar, FormTambahPelanggar
from sqlalchemy import func

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
            sql_pelanggar = (
                db.session.query(PelanggaranModel)
                .order_by(PelanggaranModel.id.desc())
                .all()
            )
            # $terbanyak = mysqli_query($connect, "SELECT detail_poin.nis, SUM(pelanggaran.poin) AS poin, siswa.nama_siswa FROM detail_poin JOIN pelanggaran ON detail_poin.id_pelanggaran=pelanggaran.id_pelanggaran JOIN siswa ON detail_poin.nis=siswa.nis GROUP BY detail_poin.nis ORDER BY SUM(pelanggaran.poin) DESC LIMIT 6");

            sql_poin = (
                db.session.query(
                    PelanggaranModel,
                    func.sum(JenisPelanggaranModel.poin_pelanggaran),
                )
                .join(JenisPelanggaranModel)
                .join(SiswaModel)
                .group_by(PelanggaranModel.siswa_id)
                .order_by(func.sum(JenisPelanggaranModel.poin_pelanggaran.desc))
                .limit(6)
            )

            response = make_response(
                render_template(
                    "guru_bk/modul/pelanggaran/daftar-pelanggar.html",
                    guru_bk=get_guru_bk(),
                    sql_pelanggar=sql_pelanggar,
                    PelanggaranModel=PelanggaranModel,
                    db=db,
                    sql_poin=sql_poin,
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
                note = request.form.get("keterangan")

                insert_pelanggar = PelanggaranModel(
                    siswaId=siswa_id,
                    jenisPelanggaranId=jenis_id,
                    pelapor=pelapor,
                    note=note,
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


@guru_bk.route("/data-pelanggaran/edit", methods=["GET", "POST"])
@login_required
def edit_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            form = FormEditPelanggar()
            id = request.args.get("idx")
            sql_pelanggaran = (
                db.session.query(PelanggaranModel).filter_by(id=id).first()
            )
            sql_jenis = JenisPelanggaranModel.query.all()
            form.siswa.data = f"{sql_pelanggaran.siswa.first_name.title()} {sql_pelanggaran.siswa.last_name.title()}"
            form.keterangan.data = sql_pelanggaran.note
            if request.method == "POST":
                siswa_id = request.form.get("siswa")
                jenis_pelanggaran_id = request.form.get("jenisPelanggaran")
                note = request.form.get("keterangan")

                sql_pelanggaran.jenis_pelanggaran_id = jenis_pelanggaran_id
                sql_pelanggaran.note = note

                db.session.commit()
                response = make_response(redirect(url_for("guru_bk.data_pelanggar")))
                flash(f"Data Telah Di Perbaharui.", "info")
                return response

            return render_template(
                "guru_bk/modul/pelanggaran/edit-pelanggar.html",
                form=form,
                guru_bk=get_guru_bk(),
                sql_jenis=sql_jenis,
                sql_pelanggaran=sql_pelanggaran,
            )
        else:
            return abort(404)


@guru_bk.route("data-pelanggaran/delete", methods=["GET", "POST"])
@login_required
def delete_data_pelanggaran():
    if current_user.is_authenticated:
        if current_user.id == get_guru_bk().guru_id:
            id = request.args.get("idx")
            sql_pelanggaran = PelanggaranModel.query.filter_by(id=id).first()

            db.session.delete(sql_pelanggaran)
            db.session.commit()

            response = make_response(redirect(url_for("guru_bk.data_pelanggar")))
            flash(f"Data Telah Di Hapus!", "error")
            return response
        else:
            return abort(404)
