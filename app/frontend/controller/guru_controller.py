from flask import (
    abort,
    request,
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
    render_template,
)
from flask_login import current_user, login_required

guru2 = Blueprint("guru2", __name__, url_prefix="/guru-site")


@guru2.route("/")
@login_required
def index():
    # if session["group"] == "guru":
    if current_user.is_authenticated:
        if current_user.group == "guru":
            return render_template("guru/index_guru.html")
        else:
            abort(404)


# else:
# abort(404)
