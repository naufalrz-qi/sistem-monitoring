from app import app
from waitress import serve
from app.extensions import login_manager
from app.models.user_model import UserModel


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


# with app.test_request_context():
#     print(url_for("login.masuk"))

if __name__ == "__main__":
    serve(app)
