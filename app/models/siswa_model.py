from app.extensions import db
import sqlalchemy as sa
from .user_model import UserModel

class SiswaModel(db.Model):
    __tablename__ = 'tb_siswa_detail'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(128), nullable=False, default='')
    last_name = sa.Column(sa.String(128), nullable=False, default='')
    gender = sa.Column(sa.String(32), nullable=False)
    tempat_lahir = sa.Column(sa.String(128), nullable=True)
    tgl_lahir = sa.Column(sa.Date(), nullable=True)
    agama = sa.Column(sa.String(128), nullable=True)
    users = db.relationship('UserModel', backref='tb_siswa_detail', lazy='dynamic')
    
    def __init__(self, first_name, last_name, gender, agama=None) -> None:
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.agama = agama
    
    
    def __repr__(self) -> str:
        return 'id user : {}'.format(self.id)