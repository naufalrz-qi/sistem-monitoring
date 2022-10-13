from app.api.controller.auth_controller import auth
from app.api.controller.siswa_controller import siswa
from app.api.controller.guru_controller import guru
from app.api.controller.master_controller import master
from app.api.controller.data_controller import data
#### SITE CONTROLLER ####
from app.site.controller.site_guru_controller import site_guru
from app.site.controller.site_staff_controller import staff


def register_bp(app):
    app.register_blueprint(auth)
    app.register_blueprint(siswa)
    app.register_blueprint(guru)
    app.register_blueprint(master)
    app.register_blueprint(data)
    app.register_blueprint(site_guru)
    app.register_blueprint(staff)