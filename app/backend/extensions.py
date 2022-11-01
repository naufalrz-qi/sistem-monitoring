from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.backend.lib.custom_model_class import IdModel

db = SQLAlchemy(model_class=IdModel)
# db = SQLAlchemy()
jwt = JWTManager()
admin = Admin(
    index_view=AdminIndexView(
        
        url='/administrator',
        # endpoint='admins'
    ),
    name='SUPER ADMIN',
    template_mode='bootstrap4',
)
migrate = Migrate()