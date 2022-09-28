from app.controller.auth_controller import auth

def register_bp(app):
    app.register_blueprint(auth)