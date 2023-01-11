from app import app
from waitress import serve
from app.extensions import login_manager
from app.models.user_login_model import UserLogin


@login_manager.user_loader
def load_user(id):
    user = UserLogin()
    user.id = id
    return user


# with app.test_request_context():
#     print(url_for("login.masuk"))

if __name__ == "__main__":
    serve(app)
