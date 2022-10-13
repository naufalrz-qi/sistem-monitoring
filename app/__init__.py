from flask import Flask
from settings import Config
from app.register_blueprint import register_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    extended_ext(app)
    extended_admin()
    register_bp(app)   
    return app 

def extended_ext(app):
    from app.extensions import db, admin, jwt, migrate
    
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    jwt.init_app(app)

def extended_admin():
    from app.super_admin.admin_model import UserView
    from app.super_admin.admin_register_views import user

app = create_app()
    