from app.extensions import db
import sqlalchemy as sa
from .user_model import UserModel
from .master_model import *
import sqlalchemy.orm as sql

class AdminDetailModel(db.Model):
    __tablename__ = 'detail_admin'
    # id = sa.Column(sa.Integer, primary_key=True)
    gender = sa.Column(sa.String(32), nullable=True)
    alamat = sa.Column(sa.String(128), nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('auth_user.id'))
    
    def __repr__(self, gender=None, alamat=None, user_id=None) -> str:
        self.gender = gender
        self.alamat = alamat
        self.user_id = user_id
            
class SiswaModel(db.Model):
    __tablename__ = 'detail_siswa'
    # id = sa.Column(sa.Integer, primary_key=True)    
    gender = sa.Column(sa.String(32), nullable=False)
    tempat_lahir = sa.Column(sa.String(128), nullable=True)
    tgl_lahir = sa.Column(sa.Date(), nullable=True)
    agama = sa.Column(sa.String(128), nullable=False, default=None)
    alamat = sa.Column(sa.String(250), nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('auth_user.id', ondelete='CASCADE', onupdate='CASCADE'))
    user = sql.relationship('UserModel', backref='users')
    
    def __init__(self, gender, agama=None, user_id=None) -> None:
        super().__init__()
        self.gender = gender
        self.agama = agama
        self.user_id = user_id
      
    def __repr__(self) -> str:
        return 'detail : {}'.format(self.first_name)

class GuruModel(db.Model):
    __tablename__ = 'detail_guru'
    # id = sa.Column(sa.Integer, primary_key=True)
    gender = sa.Column(sa.String(32), nullable=False)
    agama = sa.Column(sa.String(32), nullable=True)
    alamat = sa.Column(sa.String(256), nullable=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('auth_user.id', ondelete='CASCADE', onupdate='CASCADE'))
    users = sql.relationship('UserModel', backref='detail_guru')
    mapel_id = sa.Column(sa.Integer, sa.ForeignKey('master_mapel.id'))
    mapel = sql.relationship('MapelModel', backref='mapels')
    kelas_id = sa.Column(sa.Integer, sa.ForeignKey('master_kelas.id'))
    kelas = sql.relationship('KelasModel', backref='class')
    
    def __init__(self, gender=None, alamat=None, agama=None, user_id=None) -> None:
        self.gender = gender
        self.alamat = alamat
        self.agama = agama
        self.user_id = user_id