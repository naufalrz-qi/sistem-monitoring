from flask import Flask
from app.api.register_app import register_app
from app.site.register_app import register_app_site
from settings import Config
from app.api.lib.date_time import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    extended_ext(app)
    extended_admin()
    register_app(app)
    register_app_site(app)
    loginManager(app)

    app.jinja_env.filters["date_indo"] = format_indo
    app.jinja_env.filters["date_indo_non_weekday"] = format_indo_non_weekday
    app.jinja_env.filters["tgl"] = day_in_date
    return app


def extended_ext(app):
    from app.extensions import db, admin, jwt, migrate

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    jwt.init_app(app)


def loginManager(app):
    from app.extensions import login_manager

    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = "auth2.login"
    login_manager.login_message = (
        f"Ma'af...!!!\\nSilahkan Login Untuk Mengakses Halaman Ini."
    )
    login_manager.login_message_category = "warning"


def extended_admin():
    from app.super_admin.admin_model import UserView
    from app.super_admin.admin_register_views import user


app = create_app()
