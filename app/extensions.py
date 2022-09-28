from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


db = SQLAlchemy()
jwt_manager = JWTManager()
# admin = Admin(template_mode='bootstrap3', name='SUPER ADMIN', endpoint='admins')
admin = Admin(
    index_view=AdminIndexView(
        
        url='/administrator',
        # endpoint='admins'
    ),
    name='SUPER ADMIN',
    template_mode='bootstrap3',
)
migrate = Migrate()