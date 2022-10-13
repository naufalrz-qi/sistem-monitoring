from app.controller.auth_controller import auth
from app.controller.siswa_controller import siswa
from app.controller.guru_controller import guru
from app.controller.master_controller import master
from app.controller.data_controller import data

def register_bp(app):
    app.register_blueprint(auth)
    app.register_blueprint(siswa)
    app.register_blueprint(guru)
    app.register_blueprint(master)
    app.register_blueprint(data)