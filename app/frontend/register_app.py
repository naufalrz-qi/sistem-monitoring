from app.frontend.controller.admin_controller import admin2
from app.frontend.controller.site_guru_controller import site_guru
from app.frontend.controller.login_controller import login

def register_app_site(app):
    app.register_blueprint(site_guru)
    app.register_blueprint(admin2)
    app.register_blueprint(login)