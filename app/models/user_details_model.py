from email.policy import default
from app.extensions import db
import sqlalchemy as sa
from .user_model import UserModel
import sqlalchemy.orm as sql

class SiswaModel(db.Model):
    __tablename__ = 'tb_siswa_detail'
    id = sa.Column(sa.Integer, primary_key=True)    
    gender = sa.Column(sa.String(32), nullable=False)
    tempat_lahir = sa.Column(sa.String(128), nullable=True)
    tgl_lahir = sa.Column(sa.Date(), nullable=True)
    agama = sa.Column(sa.String(128), nullable=False, default=None)
    alamat = sa.Column(sa.String(250), nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('auth_user.id', ondelete='CASCADE', onupdate='CASCADE'))
    users = sql.relationship('UserModel', backref='detail_siswa')
    
    def __init__(self, gender, agama=None, user_id=None) -> None:
        super().__init__()
        self.gender = gender
        self.agama = agama
        self.user_id = user_id
    
    
    def __repr__(self) -> str:
        return 'detail : {}'.format(self.first_name)

class GuruModel(db.Model):
    __tablename__ = 'tb_guru_detail'
    id = sa.Column(sa.Integer, primary_key=True)
    gender = sa.Column(sa.String(32), nullable=False)
    alamat = sa.Column(sa.String(256), nullable=True)
    agama = sa.Column(sa.String(32), nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('auth_user.id', ondelete='CASCADE', onupdate='CASCADE'))
    users = sql.relationship('UserModel', backref='detail_guru')
    
    def __init__(self, gender=None, alamat=None, agama=None, user_id=None) -> None:
        self.gender = gender
        self.alamat = alamat
        self.agama = agama
        self.user_id = user_id