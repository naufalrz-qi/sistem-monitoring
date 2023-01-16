from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    make_response,
)
from flask_login import login_required, current_user
from app.models.master_model import GuruBKModel

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
    response = make_response(
        render_template("guru_bk/index_bk.html", guru_bk=get_guru_bk())
    )
    return response
