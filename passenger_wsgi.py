from app import app
from app.frontend.lib.template_filter import format_date_indo
from waitress import serve
from app.frontend.extensions import login_manager
from app.frontend.models.user_login_model import UserLogin


@login_manager.user_loader
def load_user(id):
    user = UserLogin()
    user.id = id
    # print(user)
    return user


if __name__ == "__main__":
    serve(app)
