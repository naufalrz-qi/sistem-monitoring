import sqlalchemy as sa
from ..extensions import db
import sqlalchemy.orm as rs
from .user_details_model import *

class KelasModel(db.Model):
    __tablename__ = 'master_kelas'
    id = sa.Column(sa.Integer, primary_key=True)
    kelas = sa.Column(sa.String(16), nullable=False)
    jml_laki = sa.Column(sa.Integer, nullable=True)
    jml_perempuan = sa.Column(sa.Integer, nullable=True)
    jml_seluruh = sa.Column(sa.Integer, nullable=True)
    
    def __init__(self, kelas) -> None:
        self.kelas = kelas
        self.jml_laki = 0
        self.jml_perempuan = 0
        self.jml_seluruh = 0
        
    def __repr__(self) -> str:
        return self.kelas

class MapelModel(db.Model):
    __tablename__ = 'master_mapel'
    id = sa.Column(sa.Integer, primary_key=True)
    mapel = sa.Column(sa.String(32), nullable=False)
    
    
    def __repr__(self) -> str:
        return self.mapel
    
class HariModel(db.Model):
    __tablename__ = 'master_hari'
    id = sa.Column(sa.Integer, primary_key=True)
    hari = sa.Column(sa.String(32), nullable=False)
    
    def __init__(self, hari):
        self.hari = hari
    
    def __repr__(self) -> str:
        return self.hari
    
class TahunAjaranModel(db.Model):
    __tablename__ = 'master_tahun_ajaran'
    id = sa.Column(sa.Integer, primary_key=True)
    th_ajaran = sa.Column(sa.String(32), nullable=False)
    is_active = sa.Column(sa.String(1), nullable=False)
    
    def __init__(self, ajaran, status=None):
        self.th_ajaran = ajaran
        self.is_active = status
    
    def __repr__(self) -> str:
        return self.th_ajaran

class SemesterModel(db.Model):
    __tablename__ = 'master_semester'
    id = sa.Column(sa.Integer, primary_key=True)
    semester = sa.Column(sa.String(32), nullable=False)
    is_active = sa.Column(sa.String(1), nullable=False)
    
    def __init__(self, semester=None, active=None) -> None:
        self.semester = semester
        self.is_active = active
        
    def __repr__(self) -> str:
        return self.semester

class WaliKelasModel(db.Model):
    __tablename__ = 'master_wali_kelas'
    id = sa.Column(sa.Integer, primary_key=True)
    guru_id = sa.Column(sa.Integer, sa.ForeignKey('detail_guru.id', ondelete='CASCADE', onupdate='CASCADE'))
    guru = rs.relationship('GuruModel', backref='wali_kelas')
    kelas_id = sa.Column(sa.Integer, sa.ForeignKey('master_kelas.id', ondelete='CASCADE', onupdate='CASCADE'))
    kelas = rs.relationship('KelasModel', backref='kelas_didik')
    
    def __repr__(self) -> str:
        return '{}'.format(self.kelas)  

class JamMengajarModel(db.Model):
    __tablename__ = 'master_jam_mengajar'
    id = sa.Column(sa.Integer, primary_key=True)
    jam = sa.Column(sa.String(32), nullable=False)
    
    def __init__(self, jam=None) -> None:
        self.jam = jam
        
    def __repr__(self) -> str:
        return 'jam : {}'.format(self.jam)
    
class MengajarModel(db.Model):
    __tablename__ = 'master_mengajar'
    id = sa.Column(sa.Integer, primary_key=True)
    kode_mengajar = sa.Column(sa.String(32), nullable=False)
    guru_id = sa.Column(sa.Integer, sa.ForeignKey('detail_guru.id', ondelete='CASCADE', onupdate='CASCADE'))
    guru = rs.relationship('GuruModel', backref='guru_mapel')
    hari_id = sa.Column(sa.Integer, sa.ForeignKey('master_hari.id', ondelete='CASCADE', onupdate='CASCADE'))
    jam_id_selesai = sa.Column(sa.Integer, sa.ForeignKey('master_jam_mengajar.id', ondelete='CASCADE', onupdate='CASCADE'))
    jam_id_mulai = sa.Column(sa.Integer, sa.ForeignKey('master_jam_mengajar.id', ondelete='CASCADE', onupdate='CASCADE'))
    kelas_id = sa.Column(sa.Integer, sa.ForeignKey('master_kelas.id', ondelete='CASCADE', onupdate='CASCADE'))
    semester_id = sa.Column(sa.Integer, sa.ForeignKey('master_semester.id', ondelete='CASCADE', onupdate='CASCADE'))
    tahun_ajaran_id = sa.Column(sa.Integer, sa.ForeignKey('master_tahun_ajaran.id', ondelete='CASCADE', onupdate='CASCADE'))
    
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.kode_mengajar
    

    