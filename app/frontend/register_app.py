from app.frontend.controller.admin_controller import admin2
from app.frontend.controller.guru_controller import guru2
from app.frontend.controller.login_controller import login


def register_app_site(app):
    app.register_blueprint(guru2)
    app.register_blueprint(admin2)
    app.register_blueprint(login)
