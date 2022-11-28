from flask import Flask
from app.backend.register_app import register_app
from app.frontend.register_app import register_app_site
from settings import Config
from app.frontend.models.user_login_model import UserLogin


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    extended_ext(app)
    extended_admin()
    register_app(app)
    register_app_site(app)
    loginManager(app)
    return app


def extended_ext(app):
    from app.backend.extensions import db, admin, jwt, migrate

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    jwt.init_app(app)


def loginManager(app):
    from app.frontend.extensions import login_manager

    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = "login.masuk"
    # login_manager.blueprint_login_views = {
    #     "guru2": "login.index",
    #     "admin2": "login.index",
    # }
    login_manager.login_message_category = "warning"


def extended_admin():
    from app.super_admin.admin_model import UserView
    from app.super_admin.admin_register_views import user


app = create_app()
