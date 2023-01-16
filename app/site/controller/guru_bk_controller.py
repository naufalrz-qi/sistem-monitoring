from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    Blueprint,
    make_response,
)

guru_bk = Blueprint(
    "guru_bk", __name__, static_folder="../static/", template_folder="../templates/"
)


@guru_bk.route("index")
def index():
    response = make_response(render_template("guru_bk/index_bk.html"))
    return response
