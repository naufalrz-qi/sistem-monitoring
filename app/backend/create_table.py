from app import app
from app.backend.extensions import db

with app.app_context():
    db.create_all()