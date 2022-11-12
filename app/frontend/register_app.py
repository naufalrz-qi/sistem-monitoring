from app.frontend.controller.admin_controller import admin2
from app.frontend.controller.site_guru_controller import site_guru

def register_app_site(app):
    app.register_blueprint(site_guru)
    app.register_blueprint(admin2)