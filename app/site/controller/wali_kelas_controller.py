from flask import Flask, url_for, request, redirect, flash, render_template, Blueprint
from flask_login import current_user
from app.backend.models.master_model import WaliKelasModel
from ...backend.extensions import db

wali_kelas = Blueprint(
    "wali_kelas",
    __name__,
    static_folder="../static/",
    url_prefix="/wali-kelas/",
    template_folder="../templates/",
)

query = lambda sql: sql


def check_wali():
    sql = query(
        sql=db.session.query(WaliKelasModel)
        .filter(WaliKelasModel.guru_id == current_user.id)
        .first()
    )
    return sql


@wali_kelas.route("/index")
def index_wali():
    wali_kelas = check_wali()
    return render_template(
        "wali_kelas/index_wali_kelas.html", wali_controller=wali_kelas
    )
