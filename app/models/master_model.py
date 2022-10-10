import sqlalchemy as sql
from app.extensions import db
import sqlalchemy.orm as rs
from .user_details_model import *

class KelasModel(db.Model):
    __tablename__ = 'master_kelas'
    # id = sql.Column(sql.Integer, primary_key=True)
    kelas = sql.Column(sql.String(16), nullable=False)
    jml_laki = sql.Column(sql.Integer, nullable=True)
    jml_perempuan = sql.Column(sql.Integer, nullable=True)
    jml_seluruh = sql.Column(sql.Integer, nullable=True)
    
    def __init__(self, kelas) -> None:
        self.kelas = kelas
        self.jml_laki = 0
        self.jml_perempuan = 0
        self.jml_seluruh = 0
        
    def __repr__(self) -> str:
        return self.kelas

class MapelModel(db.Model):
    __tablename__ = 'master_mapel'
    # id = sql.Column(sql.Integer, primary_key=True)
    mapel = sql.Column(sql.String(32), nullable=False)
    
    
    def __repr__(self) -> str:
        return self.mapel
    
class HariModel(db.Model):
    __tablename__ = 'master_hari'
    # id = sql.Column(sql.Integer, primary_key=True)
    hari = sql.Column(sql.String(32), nullable=False)
    
    def __init__(self, hari):
        self.hari = hari
    
    def __repr__(self) -> str:
        return self.hari
    
class TahunAjaranModel(db.Model):
    __tablename__ = 'master_tahun_ajaran'
    # id = sql.Column(sql.Integer, primary_key=True)
    th_ajaran = sql.Column(sql.String(32), nullable=False)
    is_active = sql.Column(sql.String(1), nullable=False)
    
    def __init__(self, ajaran):
        self.th_ajaran = ajaran
        self.is_active = 0
    
    def __repr__(self) -> str:
        return self.th_ajaran

class SemesterModel(db.Model):
    __tablename__ = 'master_semester'
    # id = sql.Column(sql.Integer, primary_key=True)
    semester = sql.Column(sql.String(32), nullable=False)
    is_active = sql.Column(sql.String(1), nullable=False)
    
    def __init__(self, semester=None, active=None) -> None:
        self.semester = semester
        self.is_active = active
        
    def __repr__(self) -> str:
        return self.semester

class WaliKelasModel(db.Model):
    __tablename__ = 'master_wali_kelas'
    # id = sql.Column(sql.Integer, primary_key=True)
    guru_id = sql.Column(sql.Integer, sql.ForeignKey('detail_guru.id', ondelete='CASCADE', onupdate='CASCADE'))
    guru = rs.relationship('GuruModel', backref='wali_kelas')
    kelas_id = sql.Column(sql.Integer, sql.ForeignKey('master_kelas.id', ondelete='CASCADE', onupdate='CASCADE'))
    kelas = rs.relationship('KelasModel', backref='kelas_didik')
    
    def __repr__(self) -> str:
        return '{}'.format(self.kelas)
    
class MengajarModel(db.Model):
    __tablename__ = 'master_mengjar'

class JamMengajarModel(db.Model):
    __tablename__ = 'master_jam_mengajar'
    jam = sql.Column(sql.String(32), nullable=False)
    
    def __init__(self, jam=None) -> None:
        self.jam = jam
        
    def __repr__(self) -> str:
        return 'jam : {}'.format(self.jam)
    