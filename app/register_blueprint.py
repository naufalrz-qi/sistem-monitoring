from app.controller.auth_controller import auth
from app.controller.siswa_controller import siswa
from app.controller.guru_controller import guru

def register_bp(app):
    app.register_blueprint(auth)
    app.register_blueprint(siswa)
    app.register_blueprint(guru)