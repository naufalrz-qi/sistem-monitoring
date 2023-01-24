from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    make_response,
)
from flask_login import login_required, current_user
from app.models.master_model import GuruBKModel
from app.models.data_model import *

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
            response = make_response(
                render_template(
                    "guru_bk/modul/pelanggaran/tambah-pelanggar.html",
                    guru_bk=get_guru_bk(),
                )
            )
            return response
        else:
            return abort(404)
