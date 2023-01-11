from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.api.lib.custom_model_class import IdModel
from flask_login import LoginManager


# db = SQLAlchemy(model_class=IdModel)
login_manager = LoginManager()
db = SQLAlchemy()
jwt = JWTManager()
admin = Admin(
    index_view=AdminIndexView(
        url="/administrator",
        # endpoint='admins'
    ),
    name="SUPER ADMIN",
    template_mode="bootstrap4",
)
migrate = Migrate()
