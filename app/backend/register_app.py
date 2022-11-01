from app.backend.controller.auth_controller import auth
from app.backend.controller.siswa_controller import siswa
from app.backend.controller.guru_controller import guru
from app.backend.controller.master_controller import master
from app.backend.controller.data_controller import data
from app.backend.controller.download_controller import download



def register_app(app):
    app.register_blueprint(auth)
    app.register_blueprint(siswa)
    app.register_blueprint(guru)
    app.register_blueprint(master)
    app.register_blueprint(data)
    app.register_blueprint(download)
